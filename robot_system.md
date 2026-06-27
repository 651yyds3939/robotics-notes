# 机器人全链路系统 (Full-Stack Robotics System)

> **使用说明**：在VS Code中打开此Markdown文件，按 `Ctrl+Shift+O`（Windows/Linux）或 `Cmd+Shift+O`（Mac）即可调出大纲面板，或点击左侧活动栏的「大纲」图标查看完整树状结构。

💡 形态学参考：关于不同形态机器人（轮式、足式、机械臂等）的运动学特性与区别，详见：👉 [跳转：机器人分类与特性对比](./robotics/robot_types.md)
## 一、感知层（传感器与感知层级 - Perception Layer）

> 💡 **架构标注**：感知层是跨越硬件物理边界的。处理高维数据（如视觉识别、点云特征）的高层感知逻辑需要巨大算力，运行于**上位机**；而处理极高实时性反馈（如IMU与编码器）的底层本体状态感知，则由**下位机**实时处理。

### 1.1 环境感知 (Exteroception)

#### 1.1.1 视觉类 (Vision)

* 单目相机 (Monocular Camera)
* 双目相机 (Stereo Camera)
* 深度相机 (RGB-D Camera，如 Kinect、Realsense)
* 激光雷达 (LiDAR - 2D/3D)
* 红外相机 (IR Camera)

#### 1.1.2 距离与测距 (Proximity & Ranging)

* 超声波传感器 (Ultrasonic)
* 飞行时间传感器 (ToF - Time of Flight)
* 红外测距 (IR Ranging)

#### 1.1.3 环境状态 (Environmental)

* 温湿度传感器
* 气压/高度计 (Barometer)
* 气体传感器

### 1.2 本体感知 (Proprioception)

#### 1.2.1 运动学状态 (Kinematics)

* 编码器 (Encoder：增量式 Incremental、绝对式 Absolute)
* 惯性测量单元 (IMU)
* 陀螺仪 (Gyroscope)
* 加速度计 (Accelerometer)

#### 1.2.2 动力学状态 (Dynamics)

* 六维力矩传感器 (6-Axis F/T Sensor - 人形机器人足端与腕部核心)
* 一维张力/拉压传感器
* 触觉传感器 (Tactile Sensor / 电子皮肤)

#### 1.2.3 全局定位 (Localization)

* RTK-GPS / GNSS
* UWB 室内定位系统
* 磁力计/电子罗盘 (Magnetometer)

### 1.3 特殊与交互传感器

#### 1.3.1 语音与声学

* 麦克风阵列 (Mic Array - 大模型语音交互必备)

#### 1.3.2 离散接触类

* 防撞边 / 触边开关 (Bumper)
* 机械限位开关 (Limit Switch)

### 1.4 高层感知算法与环境理解【运行于：上位机】

* **深度学习视觉感知 (Deep Learning)** 👉 [跳转：AI视觉与深度学习笔记](./ai/deep_learning_vision.md)

  * YOLOv8 / Detectron2：用于实时目标检测与实例分割，将非结构化的像素转化为结构化的语义边界框。
  * PointNet：用于 3D 激光雷达点云的特征提取与空间物体分类。
* **视觉处理基础**：OpenCV (图像处理、特征提取)
* **硬件 SDK**：Intel RealSense SDK, 各类 Lidar SDK (点云获取与解析)

### 1.5 底层状态估计与预处理【运行于：下位机】 👉 [跳转：状态估计与滤波笔记](./robotics/state_estimation.md)

* **时钟同步 (Time Synchronization)**：PTP (精确时间协议), NTP (多传感器高频数据对齐前提)
* **系统标定 (Calibration)**：相机内参标定、手眼标定 (Hand-Eye Calibration)、多传感器联合外参标定
* **状态融合与滤波**：利用卡尔曼滤波 (Kalman Filter) 等传统机器学习概率推断算法，实时融合 IMU 与关节里程计数据，提供平滑的底盘位姿反馈。

### 1.6 数据采集与遥操作平台 (Data Collection & Teleoperation)

* **动捕系统 (Motion Capture)**：OptiTrack / Vicon 等高精度光学动捕
* **VR 遥操作与映射 (VR Teleoperation Mapping)**：Apple Vision Pro / Meta Quest 结合视觉进行全身重定向映射
* **多模态数据对齐录制**：ROS 2 rosbag2 (高频同步记录视觉、本体及动作标签数据，为模仿学习与端到端训练提供基础)

---

## 二、决策层（上位机系统 / “大脑” - High-level Decision System）

> **架构演进说明**：上位机负责处理“看得懂什么”和“想干什么”。在具身智能/人形机器人中，它是处理多模态大语言模型、深度视觉感知和高级任务规划的物理载体（大脑皮层）。

### 2.1 计算硬件平台演进 (Computing Hardware)

#### 2.1.1 经典上位机 (适用于小车/轻量级机器人)

* 单板计算机 (SBC)：树莓派 (Raspberry Pi)、Rockchip RK3588等
* 低功耗边缘计算盒

#### 2.1.2 大算力上位机 (适用于人形/具身智能机器人头部)

* Nvidia Jetson 高级系列 (AGX Orin)
* x86 高性能迷你主机 (如 Intel NUC i7/i9)
* 标准工作站 / 独立显卡平台 (用于本地大模型与强感知模型推理)

#### 2.1.3 硬件加速单元

* FPGA 开发板
* AI NPU/TPU 算力棒

### 2.2 操作系统与运行环境 (OS & Middleware)

#### 2.2.1 通用操作系统 (GPOS)

* Ubuntu / Debian (Linux 核心，非强实时要求)
* Yocto (定制化嵌入式 Linux)

#### 2.2.2 机器人中间件与抽象层 (Middleware & Abstraction)

* ROS 2 (Humble / Iron - DDS通信机制) 👉 [跳转：ROS通信原理详解](./robotics/ros_communication.md) | 👉 [跳转：ROS2 开发流程笔记](./robotics/ros2_process.md)
* ROS 1 (Noetic - 主从节点机制)
* **ros2_control**：核心硬件抽象层 (统一管理硬件接口与控制器，是实现真实硬件驱动与仿真环境平滑切换的关键桥梁)

### 2.3 核心算法功能与框架 (Core Algorithms & Frameworks)

#### 2.3.1 具身智能与高层认知 (Embodied AI & High-Level Cognition) 👉 [跳转：大模型与模仿学习笔记](./ai/llm_imitation_learning.md)

* **大语言/视觉模型 (LLMs / VLMs)**：作为系统的逻辑指挥官，具备人类物理常识，负责处理人类模糊自然语言指令，并生成零代码的离散任务序列节点（如将“给我拿个解渴的”拆解为导航与抓取步骤）。
* **模仿学习 (Imitation Learning - IL)**：基于人类专家遥操作数据的行为克隆 (BC)。它解决难以建立精确物理模型的复杂灵巧操作问题，通过深度神经网络将视觉输入（相机画面）直接映射为机械臂的丝滑输出动作。
* **深度学习基础设施**：PyTorch / TensorFlow / TensorRT (支撑感知与认知模型的训练和边缘推理)。

#### 2.3.2 导航与建图 (Navigation & Mapping)

* **核心栈**：ROS Navigation / Nav2 (轮式/履带机器人全栈路径规划和避障)
* SLAM (同步定位与建图: 激光2D/3D, V-SLAM)

#### 2.3.3 机械臂与运动规划 (Manipulation)

* **核心栈**：ROS MoveIt / MoveIt 2 (官方机械臂运动规划、碰撞检测与逆向运动学)
* PyRobot (高层级 Python 机器人操作库)

#### 2.3.4 高级规划与逻辑编排 (Planning & AI Agents)

* 行为树决策 (Behavior Trees) / 状态机 (State Machine)
* **AI Agent / 工作流编排**：LangChain, CrewAI, n8n (自动触发任务、传感器数据大语言模型处理协作)

### 2.4 人机交互系统 (Human-Robot Interaction - HRI)

* **显式交互 (Explicit)**：语音指令输入、手柄/摇杆控制、UI/Web 监控界面
* **隐式交互 (Implicit)**：人体意图预测 (Human Intention Prediction)、手势识别、目光/头部姿态跟随

---

## 三、控制层（下位机系统 / “小脑” - Low-level Motion Control System）

> **架构演进说明**：下位机负责“怎么动得稳”。在双足与人形机器人中，它进化为一台运行强实时操作系统的高性能主机，负责高频执行底层动力学控制与保底安全逻辑。

### 3.1 控制硬件平台演进 (Control Boards)

#### 3.1.1 经典单片机架构 (适用于小车/普通轮式底盘)

* ARM Cortex-M 系列微控制器 (STM32 等)
* ESP32 (带无线功能，常用于节点级通讯控制)
* Arduino (AVR)

#### 3.1.2 高性能PC级架构 (适用于人形/多足机器人胸部)

* **高性能 x86 主机 (如胸部 NUC)**：作为机器人整体姿态控制的小脑，充当 ROS Master。
* 工业 PLC / 专用多轴运动控制卡

#### 3.1.3 定制化底板 (Carrier Boards)

* 传感器接口板 / 信号隔离板
* 电源分配与控制一体板

### 3.2 操作系统与通信层 (OS & Communication)

#### 3.2.1 实时操作系统 (RTOS / 硬实时)

* **宏内核实时化**：RT-Preempt (带有实时补丁的 Linux 内核，运行于 PC 级 x86/ARM 架构，人形机器人小脑必备)
* **微控制器 RTOS**：FreeRTOS / RT-Thread (MCU常用，运行于单片机/单关节驱动板)
* VxWorks (商用高可靠实时系统)

#### 3.2.2 高速总线主站 (Bus Master)

* EtherCAT 主站 (高频下发控制指令到全身几十个关节)
* CAN / CAN FD 主站

### 3.3 核心逻辑与算法 (Core Logic)

#### 3.3.1 经典闭环控制 (针对简单平台)

* 独立关节 PID 控制律 / 常用 Python & C++ 调参控制库
* 底盘运动学逆解算 (如差速、全向轮解算)
* 里程计推算 (Odometry Calculation)

#### 3.3.2 高阶动力学与平衡控制 (针对人形/足式等复杂平台) 👉 [跳转：经典动力学与运动控制笔记](./robotics/dynamics_control.md)

* 全身控制算法 (WBC - Whole-Body Control)
* 复杂运动学逆解 (IK - Inverse Kinematics)
* 模型预测控制 (MPC - Model Predictive Control)
* 质心运动学规划 / 零矩点 (ZMP) 动态平衡维持

#### 3.3.3 数据驱动的底层运动控制 (Data-Driven Locomotion) 👉 [跳转：强化学习与底层控制笔记](./robotics/RL.md) 

* **强化学习策略 (Reinforcement Learning - RL)**：作为机器人的盲走小脑。通过在物理引擎中经历亿万次的试错，提炼出超越人类手写规则的抗扰动步态。依靠状态反馈网络直接输出期望关节角度或期望蹬地接触力。
* **经典与AI混合级联架构 (Hybrid Cascade Architecture)**：现代人形的绝对主流。强化学习（RL）充当高频直觉大脑输出宏观动作倾向，全身控制（WBC）与模型预测（MPC）等经典控制作为脊髓，在极高频（~1000Hz）利用雅可比矩阵、摩擦锥与电机极限对 RL 指令进行合规审查与物理安全兜底。

---

## 四、执行层（执行器系统 / “神经末梢与肌肉” - Actuator System）

### 4.1 驱动级控制 (Motor Control)

* **4.1.1 关节级微控制器 (内嵌 MCU)**

  * 每个电机自带的微型伺服驱动板，负责接收高频指令并执行底层闭环。
* **4.1.2 驱动控制算法**

  * 矢量控制 (FOC - Field Oriented Control) —— *心脏算法，现代机器人关节的绝对核心，高频电流闭环*
  * 方波控制 (Trapezoidal / 六步换相) —— *(主要用于非精密驱动，现代复杂机器人已极少使用)*
  * 步进脉冲控制
* **4.1.3 功率变换电路 (Power Electronics)**

  * MOSFET/IGBT 逆变桥 (Inverter Bridge)
  * 预驱动电路 (Gate Driver)

### 4.2 运动执行器 (Motion Actuators)

#### 4.2.1 旋转类 (Rotary)

* 高扭矩无框力矩电机 (Frameless Motor - 人形关节主流)
* 直流无刷电机 (BLDC) / 永磁同步电机 (PMSM)
* 伺服电机系统 (Servo System)

#### 4.2.2 直线与流体类 (Linear & Fluid)

* 直线电机 (Linear Motor)
* 电动推杆 (Linear Actuator) / 滚珠丝杠模组
* 气缸 (Pneumatic Cylinder) 与 气动肌肉 (PAM)

### 4.3 传动与关节模组 (Transmission & Joints)

#### 4.3.1 精密减速器 (Precision Reducers)

* 谐波减速器 (Harmonic Drive) —— *机械臂/双足高精轻量化传动*
* RV 减速器 (Rotary Vector) —— *高负载传动*
* 行星减速器 (Planetary Gearbox) —— *机器狗关节常用*

#### 4.3.2 一体化关节 (Actuator Module)

* 减速器+电机+编码器+驱动板高度集成模块 (如准直驱关节 / 串联弹性驱动器 SEA)

#### 4.3.3 关节安全与制动装置 (Safety & Braking)

* 电磁抱闸 (Electromagnetic Brake - 断电锁死保护)
* 机械限位挡块 (Mechanical Stop)

### 4.4 操作与末端执行器 (Manipulators)

* 灵巧手 (Dexterous Hand - 多指独立驱动)
* 机械平行夹爪 (Parallel Gripper)
* 柔性抓取器 (Soft Gripper)
* 真空吸盘 (Vacuum Cup)

### 4.5 辅助执行器 (Auxiliary)

* 声光指示 (LED / 蜂鸣器 Buzzer)
* 继电器 (Relay) / 电磁阀 (Solenoid Valve)

---

## 五、机械结构层 (Mechanical Structure Layer)

### 5.1 承载主体 (Chassis & Frame)

#### 5.1.1 移动形态 (Mobile Chassis)

* 轮式 (差速 Differential、全向 Omni/Mecanum)
* 履带式 (Tracked)
* 腿式 (单足、双足人形 Bipedal、四足狗 Quadruped)

#### 5.1.2 骨架与外壳 (Frame & Shell)

* 航空级铝合金切削件 / 碳纤维框架 (轻量化高刚度需求)
* 3D 打印 / 注塑 / 玻璃钢外壳

### 5.2 宏观传动机构 (Macro Transmission)

* 同步带传动 (Timing Belt)
* 齿轮齿条 (Gear & Rack)
* 连杆机构 (Linkage Mechanism - 四足/双足腿部常见)
* 钢丝绳传动 (Tendon-driven - 灵巧手常用)

### 5.3 结构辅助件 (Hardware Fasteners)

* 精密轴承 (交叉滚子轴承、角接触轴承)
* 联轴器 (Couplings)
* 减震器 (Shock Absorbers / 阻尼器)

---

## 六、系统安全与防护机制 (Safety & Security)

> **说明**：贯穿全身软硬件的底层红线，确保机器人与人类环境交互时的绝对物理与网络安全。

### 6.1 软件与控制层安全 (Software & Control Safety)

* 看门狗定时器 (Watchdog Timer - 死机自动重启/锁死保护)
* 异常状态机 (Fault State Machine - 故障分级响应与紧急停止)
* 碰撞检测与柔顺控制 (Collision Detection & Compliance - 遇到异常阻力自动变软)
* 关节软限位 (Software Joint Limits - 动态限制最大角度/速度/力矩)

### 6.2 网络与通信安全 (Cybersecurity)

* ROS 2 SROS/DDS 加密与访问控制机制 (防止控制节点被恶意劫持)
* 局域网隔离与高频控制网络防火墙策略

---

## 七、通信系统 (Communication System)

### 7.1 内部总线与网络 (Internal Bus)

#### 7.1.1 高速硬实时总线 (小脑与全身关节通信)

* EtherCAT (微秒级同步，支持星型/链型拓扑)
* CAN / CAN FD 总线 (毫秒级同步)

#### 7.1.2 板级与外设通信 (Board-Level)

* UART (串口) / USB / SPI / I2C / I3S

#### 7.1.3 大脑与小脑通信网络 (Upper to Lower)

> 💡 **深度解析**：关于具体的网络配置、代理共享原理与排故细节，请参阅：👉 [跳转：上下位机通信与网络配置笔记](./robotics/upper_lower_communication.md)

* 物理连接层 (Physical)
  * 内部千兆以太网 (集成于机身骨架，保障物理带宽)
  * 静态 IP 局域网分配 (下位机 192.168.26.11，上位机 192.168.26.12)
  * 网络共享模式 (下位机开启 Allow LAN 代理共享)
* 传输协议层 (Transport)
  * UDP 通信 (追求极低延迟，用于高频控制律与状态下发)
  * TCP 通信 (追求可靠到达，用于建图数据与配置指令)
  * SSH / SFTP (用于开发者远程命令行调试与局域网文件传输)
* 应用框架层 (Application)
  * ROS 2 中间件 (依赖 DDS 机制实现无中心化节点发现)
  * Topic 机制 (处理异步高频数据流，如 /cmd_vel 速度指令)
  * Service 机制 (处理同步触发请求，如硬件标定与复位指令)
  * TF Tree 坐标系转换 (如相机坐标系至躯干坐标系的实时演算)
* 核心数据流向 (Data Flow)
  * 大脑下发至小脑：视觉目标 3D 坐标、大模型离散任务序列、模式切换指令
  * 小脑回传至大脑：高频底盘状态估计 (Odometry)、底层硬件异常与防撞急停报警

### 7.2 外部遥测与交互 (Telemetry & External)

* Wi-Fi (局域网SSH调试 / ROS主从机无线外链)
* Bluetooth (蓝牙手柄接入)
* 4G/5G 蜂窝网络 (云端大脑/大模型API远程接入)

---

## 八、电源系统 (Power System)

### 8.1 能源储备 (Energy Storage)

* 高倍率动力锂电池组 (Li-ion/LiPo Pack - 满足人形机器人瞬间爆发大电流)
* 超级电容 (Supercapacitor - 瞬时动态充放电补偿)
* 电池热管理系统 (液冷/风冷散热结构)

### 8.2 电池管理系统 (BMS - Battery Management System)

* 电芯均衡控制 (Cell Balancing) / 充放电保护
* 智能电量计 (SOC / SOH 状态高精度估算与实时上报)

### 8.3 电源转换与分配 (Power Distribution)

* PDU (高频开关电源分配单元 Power Distribution Unit)
* 多路 DC-DC 降压模块 (48V/24V转12V/5V/3.3V) / 升压模块
* 急停开关 (E-Stop) 与 快熔断器 (Fuse) —— *需采用逻辑电与动力电分离架构，拍下急停仅切断高压电机动力，保留低压逻辑控制电以记录故障日志并维持网络*

---

## 九、开发、测试与工程化环境 (DevOps & Toolchain) 👉 [跳转：环境相关笔记](./robotics/environment.md)

> **说明**：支持算法迭代、虚拟训练与工程部署的基础设施，现代化机器人开发必须依靠强大的工具链闭环。

### 9.1 AI 原生开发环境与 IDE (AI-Native IDEs)

* **全局库理解与多模块**：Cursor (Agent 自动生成代码、调试跨包依赖结构)
* **团队协作与原型**：Windsurf (快速原型开发), Replit Ghostwriter (云端部署/协作)
* **插件级辅助**：VS Code + GitHub Copilot / JetBrains + Codex (日常模块化补全)

### 9.2 物理仿真环境与 Sim-to-Real 闭环 (Simulators & RL Environments) 👉 [跳转：物理仿真与 Sim-to-Real 笔记](./ai/sim_to_real.md)

* **MuJoCo**：强动力学引擎，因计算开销极低，成为大规模强化学习训练“盲走策略”的首选物理平台。
* **Isaac Sim / Gazebo**：提供强大的光线追踪渲染与 GPU 并行加速能力。Isaac Sim 是目前解决“视觉感知模型”强化学习验证与合成数据生成的绝对核心工具。
* **域随机化引擎 (Domain Randomization)**：Sim-to-Real 跨越虚实鸿沟的核心武器。在训练中主动对机器人质量、摩擦系数、电机延迟注入随机噪声，确保仿真练出的 AI 具备极强的现实鲁棒性。
* **经典架构仿真**：Webots / AWS RoboMaker (用于大尺度导航集群验证)。

### 9.3 调试、监控与可视化 (Debugging & Profiling)

* **状态可视化**：RViz (ROS 三维空间呈现)
* **日志与图表**：ROS logging, rqt_console (节点调试), Matplotlib / Plotly / PlotJuggler
* **现代仪表盘**：Foxglove Studio (全功能、跨平台数据面板)
* **性能分析 (Profiling)**：Py-Spy (Python分析), NVIDIA Nsight (CUDA与渲染性能调优瓶颈分析)

### 9.4 部署、版本控制与 CI/CD (Deployment & CI/CD)

* **容器化部署与环境隔离**：Docker / Docker Compose / DevContainers (开发容器，统一团队依赖，保证宿主机整洁) 👉 [跳转：docker笔记](./robotics/docker.md)
* **版本控制**：Git / GitHub / GitLab 👉 [跳转：git/github笔记](./robotics/git_github.md)
* **自动化工作流 (CI/CD)**：GitHub Actions / GitLab CI (自动代码构建、自动化跑仿真测试管道)

### 9.5 文档生成与项目管理 (Docs & Management)

* **文档自动化**：Sphinx / MkDocs (生成模块接口与代码说明文档)
* **架构绘图**：Draw.io / Mermaid (绘制状态机、节点依赖图与系统架构图)
* **任务规划**：Jira / Trello / Notion (迭代计划与Bug追踪)
