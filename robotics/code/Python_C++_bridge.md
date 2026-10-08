---
> **📌 文档定位：** 通用分工地图 — 机器人二次开发中 Python 与 C++ 各自负责什么
> **适合：** 刚接触 ROS 机器人开发，不清楚该写 `.py` 还是该碰 `.cpp` 的开发者
> **前置：** 无（建议先浏览 [README.md](README.md) · [robot_system.md](../../robot_system.md)）
> **后续：** Python 二次开发 → [robotics_C++.md](robotics_C++.md)（读底层时）· [ros_logic.md](../ros_logic.md)
> **预计时间：** 30 min 通读
> **🏠 返回总索引：** [README.md](README.md)

# 🐍⚡ 机器人二次开发：Python 与 C++ 分工指南

> **链接规范**（与 [robot_system.md](../../robot_system.md) 一致）
>
> - **👉 专题笔记** → 本仓库 [`robotics/`](../)（相对路径）
> - **👉 实战案例** → [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（**GitHub 绝对链接**）

> **核心结论：**
>
> 在大多数商用/开源机器人的**二次开发**场景中，**应用层代码以 Python 为主**。
>
> 开发者通常不是去改电机力矩环，而是**查阅官方 SDK 接口 → 用 Python 发布 ROS 话题 / 调用服务 → 把感知、大模型、抓取、任务流程组装起来**。
> C++ 主要在厂商或官方已写好的**控制底座**里运行；二次开发者**调用它**，而不是**从零重写它**。

---

## 一、什么是「二次开发」？和底层 C++ 的关系

把机器人软件栈抽象为 **三层**（适用于人形、轮式、机械臂等形态）：

```text
┌─────────────────────────────────────────────────────────────────┐
│  L2  二次开发层（应用开发者主要工作区）          【Python 为主】     │
│      rospy / rclpy 节点 · SDK 脚本 · YOLO/LLM · 行为树 · 采数   │
│      查官方接口文档 → 发 Topic/Service → 拼业务流程              │
├─────────────────────────────────────────────────────────────────┤
│  L1  官方开源应用层（可改，但多数时候只配置/编译） 【C++ + 配置】   │
│      控制器编排 · IK/规划服务 · demo 包 · MPC 配置 · launch/URDF │
├─────────────────────────────────────────────────────────────────┤
│  L0  厂商闭源控制底座（不要改，甚至看不到源码）    【C++ 二进制】   │
│      全身控制器 · 硬件抽象层 · 现场总线主站 · kHz 级伺服环          │
└─────────────────────────────────────────────────────────────────┘
```

| 层级 | 你要做什么 | 主要语言 | 专题 |
| --- | --- | --- | --- |
| **L2 二次开发** | 写业务：抓取、语音、VLA、跟随、录数据 | **Python** | [ROS 架构逻辑](../ros_logic.md) |
| **L1 官方应用** | 改 launch、改配置、偶尔改 demo 包、`catkin build` | C++ 配置为主 | [ROS2 开发流程](../ros2_process.md) |
| **L0 控制底座** | **不修改**；知道存在即可 | C++（常闭源） | [经典动力学与控制](../dynamics_control.md) |

👉 **实战案例**：[第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md) · [开源/闭源边界说明](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/0.1.example.md) · [SDK 接口使用文档](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/接口使用文档.md)

---

## 二、为什么二次开发大多是 Python？

不是 Python「比 C++ 更适合机器人」，而是**行业惯例把二次开发入口设计在了 Python + ROS 接口上**：

| 原因 | 说明 |
| --- | --- |
| **官方 SDK 多用 Python 示例** | 厂商文档、Demo、`examples/` 目录以 `rospy` / `rclpy` 为主 |
| **控制底座已封装** | 站立、行走、平衡、轨迹跟踪已在 C++ 节点中运行；应用层发速度/关节指令即可 |
| **AI 生态在 Python** | YOLO、PyTorch、LLM、LeRobot、仿真训练 toolchain 全在 Python |
| **迭代速度** | 改 Prompt、改检测类别、改状态机，Python 改完即跑，无需重新编译整个工作空间 |
| **闭源边界** | 力矩环、全身控制核心往往**改不了**；写 C++ 也进不了 L0 |

**二次开发的典型工作流：**

```text
1. 打开官方《接口使用文档》查话题名和消息类型
2. 写 Python 脚本：Publisher / ServiceProxy / ActionClient
3. launch 拉起官方 C++ 控制栈（通常不用自己写）
4. python3 your_node.py 发指令
5. rosbag / 日志 / 脚本排障
```

👉 **实战案例**：[第一个 ROS 节点（头部控制四步法）](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)

---

## 三、双机架构：上位机 vs 下位机（二次开发视角）

许多机器人采用**上位机 + 下位机**双计算单元（如 x86 工控机 + 边缘 AI 板），通过 ROS 组网。

```text
┌──────────────────── 上位机（边缘 AI 板 / GPU 主机）────────────────────┐
│  【Python 二次开发主战场 — 感知 / AI / 交互】                            │
│  · 相机驱动 · 目标检测 · 人脸/跟踪 · ASR/LLM · 多模态网关                │
│  · VLA 主控脚本 · 模仿学习数据采集 · 视觉抓取节点                         │
│  · HTTP / UDP 与下位机通信                                              │
└───────────────────────────────┬────────────────────────────────────────┘
                                │ ROS Topic / Service / HTTP
┌───────────────────────────────▼────────────────────────────────────────┐
│  下位机（实时工控机）                                                    │
│  【C++ 控制底座 + Python 二次开发节点并存】                               │
│  C++ 在跑（通常不写）：主控制器 · MPC/WBC · IK 服务 · 硬件驱动            │
│  Python 在写：轨迹编排 · 遥控逻辑 · demo 脚本 · 部署切换 · bag 分析       │
└────────────────────────────────────────────────────────────────────────┘
```

**对二次开发者的含义：**

- 做 **视觉 / 语音 / VLA / 大模型** → 主要在上位机写 **Python**
- 做 **手臂 / 底盘 / 抓取 / IK 调用** → 在下位机写 **Python**（调用 C++ 提供的 Service）
- **不需要**自己写 WBC/MPC，只要**会调接口**

👉 **实战案例**：[上下位机网络配置](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/16.Internet.md) · [VLA 视听觉全闭环抓取（多终端架构）](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md)

---

## 四、按开发主题：该用 Python 还是 C++

### 4.1 几乎 100% Python 的主题（二次开发核心）

| 主题 | 典型工作 | 专题 |
| --- | --- | --- |
| **第一个 ROS 节点** | `rospy` / `rclpy` 发布控制指令 | [ROS 通信原理](../ros_communication.md) |
| **官方 SDK 调用** | 查文档、Topic/Service 示例 | [ROS 架构逻辑](../ros_logic.md) |
| **目标检测 / 视觉** | 训练、推理、TF 坐标发布 | [视觉基础模型](../vision_foundation_models.md) |
| **VLA / 语音抓取** | LLM + 检测 + IK 全流程编排 | [VLA 研究版图](../vla_landscape.md) |
| **大模型 / 语音交互** | ASR、TTS、本地/云端 LLM | [语音全链路](../speech_pipeline.md) · [LLM for Robotics](../llm_for_robotics.md) |
| **人脸 / 视觉跟随** | 检测 + 跟踪 + 底盘/头部协同 | [视觉基础模型](../vision_foundation_models.md) |
| **模仿学习 / 数据采集** | LeRobot、ACT、遥操作录数据 | [Benchmark 与 Dataset](../benchmark_dataset.md) |
| **动捕 / 多模态输入** | 相机、VR、Webcam 接入 | [Benchmark 与 Dataset](../benchmark_dataset.md) |
| **RL / 世界模型训练** | Isaac Lab、PPO、TD-MPC2 等 | [RL 笔记](../RL.md) · [世界模型](../world_model.md) |
| **排障 / 数据分析** | rosbag 解析、Python 分析脚本 | [代码阅读技能](../code_read_skill.md) |
| **多终端编排** | launch、IP 配置、点火序列 | [robot_software_pipelines](../robot_software_pipelines.md) |

👉 **实战案例**：[YOLO 仿真](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.2yolov8_sim.md) · [真机 YOLO 环境](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.3.real_robot_yolo_environment.md) · [VLA 22.1–22.4 系列](https://github.com/651yyds3939/kuavo-dev-notes/tree/master/kuavo_notes) · [LeRobot 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) · [Isaac Lab 行走训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md) · [舞蹈 RL 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.4.RL_dance_train.md)

---

### 4.2 Python 为主、偶尔碰 C++ 配置的主题

| 主题 | Python 做什么 | C++ 涉及什么 | 专题 |
| --- | --- | --- | --- |
| **手臂 / IK 抓取** | 调 IK Service，发布关节轨迹 | IK/规划节点本身为 C++ | [MoveIt 专题](../moveit_manipulation.md) |
| **MoveIt 抓取** | Python 发目标、调 launch | MoveIt 栈为 C++，主要改 launch/配置 | [MoveIt 专题](../moveit_manipulation.md) |
| **导航 / 建图** | launch、参数、Docker 挂载 | SLAM/导航栈为 C++ | [SLAM](../slam.md) · [路径规划](../path_planning.md) |
| **RL Sim2Sim / 部署对齐** | Python 改训练配置、分析脚本 | 对齐 C++ 控制器观测空间 | [RL](../RL.md) · [边缘部署](../edge_deployment.md) |
| **全身动作 / 舞蹈** | Python 编轨迹、CSV、终端编排 | 底层执行在 C++ 控制器 | [经典动力学与控制](../dynamics_control.md) |
| **示教 / 标定** | 脚本触发、数据处理 | 部分补偿/驱动为 C++ 包 | [相机标定](../camera_calibration.md) |

**原则：** C++ 部分当**黑盒服务**；通过 ROS 接口和配置文件与之交互。

👉 **实战案例**：[IK 逆运动学](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/9.IK.md) · [视觉抓取基础](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/6.visual_grasp.md) · [MoveIt 双轨抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/28.moveit_grasping.md) · [地图导航与 FAST-LIO](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/3.map_navigation.md) · [MuJoCo Sim2Sim](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.3RL_lab_sim_to_sim.md) · [关节标定](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/26.joint_calibration.md)

---

### 4.3 主要是「编译 / 部署 / 读码」的 C++ 主题

这些场景里 **Python 仍占大量篇幅**（训练、终端、分析），但**上真机或对齐观测空间**时必须理解 C++ 侧：

| 主题 | C++ 在干什么 | 你要会什么 | 专题 |
| --- | --- | --- | --- |
| **行走 Sim2Real** | 主控制器加载 ONNX 策略 | `catkin build`、launch、obs 维度对齐 | [边缘部署](../edge_deployment.md) |
| **舞蹈/全身 RL 真机** | C++ 控制器 + Python 混合调试 | 读配置、Python bag 分析 | [RL](../RL.md) |
| **工作空间编译** | 整个 catkin/colcon 工作空间 | Docker 里编译主控包 | [Docker](../docker.md) · [环境](../environment.md) |
| **仓库结构理解** | 哪些目录是 C++ 包 | 知道去哪找，不必全读懂 | [工作空间文件速查](../doc_concept.md) |

**RL 部署链（行业通用）：**

```text
Python 训练 (仿真器)     →  .pt / checkpoint
Python 导出            →  .onnx
C++ 控制器加载 ONNX     →  50~100Hz 真机推理
Python 脚本            →  终端点火、遥控、bag 分析
```

👉 **实战案例**：[行走 Sim2Real 真机部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) · [舞蹈真机混合部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.7.RL_dance_deploy_hybrid.md) · [仿真环境部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/1.start.md) · [仓库结构导读](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/0.doc.md)

---

### 4.4 应用开发者基本不写的 C++（闭源底座）

许多整机厂商会将以下来源 **闭源分发**（预编译 `.so`），二次开发**不应试图修改**：

| 模块类型 | 典型内容 | 二次开发策略 |
| --- | --- | --- |
| 硬件抽象层 (HAL) | 电机驱动、传感器驱动 | **不修改** |
| 全身控制器 (WBC) | 力矩分配、平衡 | **不修改** |
| 现场总线主站 | EtherCAT / CAN 周期通信 | **不修改** |
| 最优控制求解器绑定 | MPC 与机型绑定的闭源部分 | 改 `.info` / 配置文件，不改内核 |

👉 **实战案例**：[开源/闭源边界与可行性评估](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/0.1.example.md)

---

## 五、二次开发最常用的 Python 模式（通用）

官方 SDK 文档是二次开发的「字典」。不同机型话题名不同，但**模式一致**：

| 想做什么 | 通用 ROS 模式 | 典型接口类型 |
| --- | --- | --- |
| 控制头部/关节 | 发布关节目标 | Topic + 自定义 msg |
| 手臂轨迹 | 发布轨迹或目标位姿 | Topic / Trajectory |
| 逆运动学 | 调用 IK 服务 | Service |
| 夹爪/末端执行器 | 发布夹爪指令 | Topic / Service |
| 底盘移动 | 发布速度或位姿 | `cmd_vel` / `cmd_pose` |
| 触发站立/模式切换 | 一次性命令 | Service / Trigger |
| 读传感器 | 订阅原始数据 | Topic |

**标准 Python 四步**（适用于 ROS 1 `rospy`，ROS 2 `rclpy` 同理）：

```python
rospy.init_node('my_node')
pub = rospy.Publisher('/target_topic', MsgType, queue_size=10)
rospy.sleep(1.0)   # 等待底层 C++ 订阅者就绪
pub.publish(msg)   # 发给 C++ 控制器执行
```

你写 Python，**执行在 C++ 底座**。

👉 **实战案例**：[第一个 ROS 节点完整模板](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md) · [SDK 接口速查（全量 Topic/Service）](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/接口使用文档.md)

---

## 六、什么时候才需要认真学 C++？

在二次开发路径下，C++ 不是「日常语言」，但以下场景**躲不开**：

| 场景 | 为什么要 C++ | 学习资源 |
| --- | --- | --- |
| **读懂控制 launch 编译报错** | `catkin build` / `colcon build` 失败 | [环境](../environment.md) · [Docker](../docker.md) |
| **RL 部署观测对齐** | 训练侧 obs 维度和 C++ 控制器必须一致 | [边缘部署](../edge_deployment.md) |
| **读主控制器源码** | Sim2Sim 不过时需要跟 C++ 逻辑 | [robotics_C++.md](robotics_C++.md) |
| **自研 C++ 行为树引擎** | 替代 Python 顶层调度，提升真机稳定性 | [Job_Requirements](Job_Requirements_for_Robot.md) |
| **改官方 C++ demo 包** | 如 BehaviorTree.CPP 搬箱案例 | [ROS 架构逻辑](../ros_logic.md) |
| **MoveIt / 导航 deep debug** | 改规划参数或插件 | [MoveIt 专题](../moveit_manipulation.md) |

**如果只做：** 视觉抓取、VLA、大模型、数据采集、跟随、简单手臂控制 → **Python 足够，先别深啃 C++**。

---

## 七、常见二次开发场景：语言选型

| 我想做… | 用什么 | 专题 / 入口 |
| --- | --- | --- |
| 让机器人做简单动作（转头/挥手） | **Python** | [ROS 通信](../ros_communication.md) |
| 检测 + 抓取 | **Python** | [VLA 版图](../vla_landscape.md) |
| 语音控制抓取 (VLA) | **Python** | [语音管线](../speech_pipeline.md) |
| 行为树编排任务 | **Python** (`py_trees`) 为主 | [ROS 架构逻辑](../ros_logic.md) |
| 录模仿学习数据 | **Python** | [Benchmark](../benchmark_dataset.md) |
| 训练行走/舞蹈 RL | **Python** | [RL](../RL.md) |
| RL 策略上真机 | **Python 部署 + C++ 推理** | [边缘部署](../edge_deployment.md) |
| 改 WBC/力矩环算法 | **通常不可行**（闭源） | — |
| 用 C++ 重写任务调度 | **C++**（工程优化方向） | [C++ 语法补充](C++_grammar_supplement.md) |

👉 **实战案例**：[视觉抓取路线概览](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.1.visual_grasping_route.md) · [行为树版 VLA](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) · [决策树专题](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/29decision_tree.md) · [舞蹈终端命令全集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.1.RL_dance_terminal_commands.md)

---

## 八、案例：分层 VLA 抓取的数据流（通用）

以典型的**分层 VLA 管线**为例（语音 → 检测 → 规划 → 执行），说明两种语言如何接力：

```text
[上位机 · Python] 相机驱动           → 发布图像 Topic
[上位机 · Python] 检测 + TF          → 输出目标 3D 坐标
[上位机 · Python] ASR + LLM + TTS    → 语音理解 + 意图解析
[上位机 · Python] VLA 主控脚本        → 编排 JSON 指令
        │ ROS Topic / HTTP
        ▼
[下位机 · C++ 已在跑] IK 服务         → Python 调 Service，不写求解器
[下位机 · C++ 已在跑] 主控制器         → 站立 / 平衡 / WBC
[下位机 · Python 可选] 轨迹发布        → 发关节轨迹 Topic
```

**二次开发者写的：** 上位机多个 Python 进程 + 下位机可能的 Python 编排。
**不需要写的：** WBC、MPC、现场总线、IK 求解器内部。

👉 **实战案例**：[VLA 视听觉全闭环抓取实录](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md) · [MCP Tool Call 版](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md)

---

## 九、决策流程（二次开发版）

```text
                我要给机器人加一个应用层功能
                              │
                              ▼
              能不能用官方 SDK 的 Topic/Service 实现？
                    │                    │
                   能                   不能
                    │                    │
                    ▼                    ▼
              写 Python               需要改 WBC/力矩环吗？
              rospy/rclpy 节点              │
              （大多数情况）           是 → 通常做不了（闭源）
                                       否 ↓
                              需要 GPU 训练 / 大模型吗？
                                    │         │
                                   是        否
                                    │         │
                                    ▼         ▼
                                 Python    需要 1kHz 实时吗？
                                 训练/AI        │        │
                                               是       否
                                                │        │
                                                ▼        ▼
                                          读 C++    Python 或
                                          部署端   改官方 demo
```

---

## 十、按控制频率选型（工业界通用规律）

| 频率范围 | 典型模块 | 推荐语言 | 原因 |
| --- | --- | --- | --- |
| **1 kHz** | 关节力矩环、EtherCAT 周期 | **C++** | Python GC 停顿不可接受 |
| **100–500 Hz** | RL 策略推理、WBC、IMU 融合 | **C++** | 需要确定性延迟 |
| **30–50 Hz** | 视觉检测、深度图处理 | **Python 或 C++** | 边缘板常用 Python+TensorRT |
| **10 Hz 以下** | 全局规划、LLM 对话 | **Python** | 逻辑复杂、迭代快 |
| **离线/训练** | 仿真器训练、数据分析 | **Python** | PyTorch 生态 |

👉 专题：[现场总线与 EtherCAT](../fieldbus_and_ethercat.md) · [多速率控制架构（robot_system §三）](../../robot_system.md)

---

## 十一、和本目录其他文档怎么配合

```text
                    Python_C++_bridge（本文）
                    「二次开发该用哪种语言」
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
  robotics/ 专题     robotics_Python     code/ C++ 系列     kuavo-dev-notes
  （通用理论）             （读/写 C++ 时）     （👉 GitHub 实战案例）
```

| 你的阶段 | 先看 | 再看 |
| --- | --- | --- |
| 零基础二次开发 | 本文 → [python_for_robotics_basics](python/python_for_robotics_basics.md) → [robotics_Python](robotics_Python.md) | 👉 [第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md) |
| 做视觉/AI 项目 | 本文 §4.1 | [AI 学习 Hub](../AI_learning_robotics.md) |
| RL 训练部署 | 本文 §4.3 | [RL](../RL.md) → 👉 [15.4 Sim2Real](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) |
| 想读控制 C++ 源码 | 本文 §4.4 | [robotics_C++.md](robotics_C++.md) |
| C++ 行为树长期目标 | 本文 §六 | [Job_Requirements](Job_Requirements_for_Robot.md) |

---

## 十二、常见误区

| 误区 | 正解 |
| --- | --- |
| 「做机器人必须先精通 C++」 | 二次开发**先精通 Python + ROS 接口** |
| 「我要改 WBC 算法」 | 闭源机型上通常**改不了**；改应用层逻辑 |
| 「所有机型都以 MoveIt 为手臂规划核心」 | 不少整机走**官方 IK 服务 + 关节轨迹 Topic** 主路径 |
| 「Python 节点能跑 1kHz 控制环」 | 不能；高频控制在 C++ 底座里 |
| 「训练用 Python，真机也用 Python 调 torch」 | 控制环内用 **ONNX + C++** |
| 「全部改成 C++ 才是专业」 | 过度工程；该 Python 的层用 Python 迭代更快 |
| 「行为树一定要 C++」 | 工程上常用 **`py_trees` Python**；C++ 行为树是性能优化方向 |

---

## 十三、总结

| | Python | C++ |
| --- | --- | --- |
| **在二次开发中的占比** | **主体**（写业务、AI、编排） | 少数（编译、部署、读码、未来行为树） |
| **你主要做什么** | 调接口、写 AI、拼流程 | 编译官方包、RL 部署对齐、读控制器 |
| **官方入口** | SDK、`demo/`、Python 示例 | 主控包、Docker 编译、闭源 `.so` |
| **能不能改力矩环** | 不能（也不该） | **通常不能**（闭源） |
| **首要学习文档** | [ROS 通信](../ros_communication.md) | [robotics_C++.md](robotics_C++.md)（需要时再学） |

> **一句话：** 机器人二次开发 = **用 Python 调用官方已经写好的 C++ 控制能力，把业务逻辑拼出来。**

---

## 📍 文档导航

| 方向 | 文档 |
| --- | --- |
| 🏠 总索引 | [README.md](README.md) |
| 全链路地图 | [robot_system.md](../../robot_system.md) |
| **Python/C++ 分工（本文）** | [Python_C++_bridge.md](Python_C++_bridge.md) |
| Python 最小语法 | [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md) |
| 读 Python 源码 | [robotics_Python.md](robotics_Python.md) |
| 读 C++ 源码 | [robotics_C++.md](robotics_C++.md) · [C++_grammar_supplement.md](C++_grammar_supplement.md) |
| ROS 专题 | [ros_logic.md](../ros_logic.md) · [ros_communication.md](../ros_communication.md) |
| RL / 部署 | [RL.md](../RL.md) · [edge_deployment.md](../edge_deployment.md) |
| 👉 机型实战索引 | [kuavo-dev-notes/kuavo_notes](https://github.com/651yyds3939/kuavo-dev-notes/tree/master/kuavo_notes) |
