# 机器人建模 (Robot Modeling) —— URDF / MJCF / USD 全解析

> **核心定位**：机器人模型是仿真与真机之间的**唯一桥梁**。URDF 定义了运动学链、惯量、碰撞几何、关节限位——一个错位的关节或错误的惯量参数，直接导致仿真训出来的策略在真机上崩溃。
>
> 👉 实战笔记：[Sim2Real URDF 缝合](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) · [S49 舞蹈 RL 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.3.RL_dance_train.md)

---

## 第 0 章：机器人建模一句话

> **大白话**：URDF 就是机器人的"出生证明"——它告诉仿真器：这个机器人有几条腿、每条腿有几节、每节多重、关节能转多少度。如果出生证明上写错了（关节顺序不对、质量偏差太大），那仿真里练出来的"肌肉记忆"套到真身上就直接摔。

---

## 第 1 章：三种主流建模格式

| 格式 | 适用场景 | 特点 |
|------|---------|------|
| **URDF** (Unified Robot Description Format) | [ROS](./ros_logic.md) 标准，MoveIt / Gazebo / [MuJoCo](./robot_modeling.md) | XML 格式，运动学链+惯量+碰撞+视觉 |
| **MJCF** (MuJoCo XML) | MuJoCo 仿真器原生格式 | 比 URDF 更灵活，支持 tendon、equality constraint |
| **USD** (Universal Scene Description) | Isaac Sim 原生格式 | Pixar 的工业级场景描述，支持物理材质、光线追踪 |

> **URDF→MJCF**：MuJoCo 可自动编译 URDF，但会丢失部分高级特性（如 tendon）。 
> **URDF→USD**：Isaac Sim 通过 URDF Importer 运行时转换，S49 训练较 S46 慢 63% 的根因（S46 用的是预烘焙 USD，S49 走运行时转换）。

---

## 第 2 章：URDF 核心结构

```xml
<robot name="kuavo_s49">
  <!-- 1. 连杆 (Link)：刚体段 -->
  <link name="torso">
    <inertial>          <!-- 质量+惯量矩阵 -->
      <mass value="15.0"/>
      <inertia ixx="0.5" iyy="0.4" izz="0.3" .../>
    </inertial>
    <visual>            <!-- 显示用，不影响物理 -->
      <geometry><mesh filename="torso.stl"/></geometry>
    </visual>
    <collision>         <!-- 碰撞检测用 -->
      <geometry><box size="0.3 0.2 0.5"/></geometry>
    </collision>
  </link>

  <!-- 2. 关节 (Joint)：连杆之间的约束 -->
  <joint name="left_shoulder_pitch" type="revolute">
    <parent link="torso"/>
    <child  link="left_upper_arm"/>
    <origin xyz="0 0.15 0.8" rpy="0 0 0"/>  <!-- 在父连杆坐标系中的安装位置 -->
    <axis   xyz="0 1 0"/>                    <!-- 旋转轴 -->
    <limit  lower="-3.14" upper="1.57"       <!-- 关节限位 -->
            effort="100" velocity="3.14"/>   <!-- 力矩/速度上限 -->
  </joint>
</robot>
```

### 2.1 关键约束

| 要素 | 如果写错 | 后果 |
|------|---------|------|
| **关节顺序** | CSV 列序 ≠ URDF 关节序 | [RL 策略](./RL.md) 收到错位的观测，训出来是僵尸站姿 |
| **质量/惯量** | 偏差 >20% | 仿真物理和真机不一致，Sim2Real 失败 |
| **关节限位** | 仿真比真机大 | 策略下发真机做不到的角度 → 电机堵转或爆冲 |
| **碰撞几何** | 为加速训练做 Lite 剥离 | 训出来的策略不避自碰撞，真机手臂打躯干 |
| **安装原点 (origin)** | xyz/rpy 错位 | 运动学链全部偏移，IK 解算出来的末端位置是错的 |

---

## 第 3 章：xacro —— URDF 的宏语言

手写几百个关节的 URDF 不现实。xacro 是 URDF 的宏扩展工具，支持变量、宏定义、数学表达式。

```xml
<!-- xacro 宏：定义一个通用关节 -->
<xacro:macro name="revolute_joint" params="name parent child origin_xyz axis lower upper">
  <joint name="${name}" type="revolute">
    <parent link="${parent}"/>
    <child  link="${child}"/>
    <origin xyz="${origin_xyz}" rpy="0 0 0"/>
    <axis   xyz="${axis}"/>
    <limit  lower="${lower}" upper="${upper}" effort="100" velocity="10"/>
  </joint>
</xacro:macro>

<!-- 批量生成双腿关节 -->
<xacro:revolute_joint name="left_hip_yaw"   parent="torso" child="left_hip" .../>
<xacro:revolute_joint name="left_hip_roll"  parent="left_hip" child="left_thigh" .../>
```

---

## 第 4 章：S49 实战——三体撕裂与手动缝合

遇到的核心问题是 **S49 真机 vs S42/S46 训练资产 vs 部署包骨架**的"三体撕裂"：

| 资产 | 版本对齐情况 | 对齐/缝合操作 |
|------|------------|-------------|
| 真机 URDF | S49 独有（26-DOF 精简链） | 手动创建 `biped_s49_26dof_lite.urdf` |
| 训练 .info 文件 | 官方只给到 S46 | 手动修改关节数、电机限位、刚度阻尼 |
| `humanoidController.cpp` | 部署侧硬编码了 S42/S46 | 手动注入 S49 关节常量 |
| CSV 动作数据 | S54 动捕数据→S49 适配 | `adapt_dance_csv.py --profile fullbody_inplace` |

> 👉 完整操作见：[Sim2Real 真机部署黑皮书](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md)

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **URDF** | ROS 标准机器人描述格式，XML |
| **xacro** | URDF 的宏扩展语言，支持变量/宏/数学表达式 |
| **MJCF** | MuJoCo 原生 XML 格式 |
| **USD** | Universal Scene Description，Isaac Sim 原生格式 |
| **Link (连杆)** | 刚体段，含质量/惯量/碰撞/视觉属性 |
| **Joint (关节)** | 连杆间的约束，定义安装位置、旋转轴、限位 |
| **Kinematic Chain** | 运动学链：从基座到末端的连杆-关节序列 |
| **Inertial** | 惯量参数：质量 + 6 个转动惯量分量 |
