# 机器人全链路系统 (Full-Stack Robotics System)

> **使用说明**（与 [README.md](./README.md) 一致）
>
> 本文件是**机器人全链路系统**的主索引，先以第 0 章说明机器人形态与系统边界，再按九大领域组织系统知识。九大领域不是严格串行的“九层协议栈”，而是四类互补视角：**运行时主链**（感知与估计 → 应用/任务/规划 → 控制 → 执行）、**物理本体**（机械与电源）、**横切能力**（安全与通信）和**研发支撑**（开发、测试与工程化）。导图内已加入可点击链接：
> - **👉 专题笔记** → 本仓库 [`robotics/`](./robotics/) / [`ubuntu/`](./ubuntu/)（相对路径）
> - **👉 实战案例** → 独立仓库 [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（**GitHub 绝对链接**；两仓库分工见 [README「链接规范」](./README.md#链接规范两仓库分工)）
>
> **推荐阅读顺序**：① 本导图建立全链路地图 → ② 按节点进专题笔记 → ③ 环境/工具查 [`ubuntu/`](./ubuntu/) → ④ 写代码用 [`ros_code_template/`](./robotics/ros_code_template/)。
>
> **三种查看方式**
>
> | 方式 | 做法 |
> |------|------|
> | **大纲视图** | VS Code / Cursor 打开本文件，按 `Ctrl+Shift+O` 浏览树状结构 |
> | **Markmap（推荐）** | 安装扩展 **Markmap** → 右键本文件 → **Open in Markmap** → 交互展开并点击链接 |
> | **浏览器离线 HTML** | 打开 [`robot_system_photo.html`](./robot_system_photo.html)（数据预渲染 + 本地 `assets/markmap/`，**无需联网**） |
>
> **HTML 离线版提示**（详见 [README「用浏览器打开 HTML 版」](./README.md#用浏览器打开-html-版离线)）：
> - 终端：`xdg-open /path/to/robotics-notes/robot_system_photo.html`（将路径改为本机实际目录）
> - 须从 **`robotics-notes/` 仓库根目录内**打开，勿单独拷贝 HTML，否则 `assets/markmap/` 会失效
> - 若主区域空白、仅见右下角工具栏：点 **「适应屏幕」**，或 `Ctrl + Shift + R` 刷新
> - 修改本 `.md` 后运行 `./regenerate_robot_system_html.sh` 可更新 HTML；完全同步仍推荐 **Markmap 直接打开本文件**
>
> 📂 **GitHub**：[robotics-notes](https://github.com/651yyds3939/robotics-notes)（本库 · 通用理论/架构/工具链）· [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（具体机型实机/仿真二次开发实战，54 篇文档）
>
> 💡 不同形态机器人 👉 [机器人分类与特性对比](./robotics/robot_types.md)
>
> 🔧 研发流程 👉 [robot_development_lifecycle.md](./robot_development_lifecycle.md) · 软件管线 👉 [robot_software_pipelines.md](./robotics/robot_software_pipelines.md) · 导航 👉 [robot_knowledge_map.md](./robot_knowledge_map.md)

---

## 零、机器人形态与系统边界 (Robot Types & Embodiment) 👉 [机器人分类与特性对比](./robotics/robot_types.md)

> 机器人形态决定运动约束、自由度、感知配置、执行器、控制方法、安全状态与验证路线；面对新平台应先分析物理约束和环境交互，而不只是外形。

### 0.0 机器人的定义
- **机器人 = 自主感知 + 自主决策 + 自主执行**，三者缺一不可
- 只有执行没有感知和决策 → 自动化设备；没有自主决策 → 遥控设备；没有物理执行 → 纯软件 AI

### 0.1 按运动与作业形态

- **地面移动**：差速 / 全向 / 阿克曼轮式、履带式
- **足式移动**：双足人形、四足及其他多足机器人
- **操作机器人**：固定串联/并联机械臂、协作机器人、双臂与灵巧手
- **移动操作**：轮式机械臂、轮式人形、双足人形等“移动 + 操作”组合
- **自动驾驶**：乘用车/商用车/物流小车，涵盖纯视觉、视觉+激光雷达、多传感器融合方案
- **特殊介质**：多旋翼/固定翼 UAV、水下 ROV/AUV，以及软体与微型机器人

### 0.2 形态决定系统约束

- **轮式**：完整或非完整运动学约束，重点是定位、导航、轨迹跟踪与地面通过性
- **足式/人形**：欠驱动浮动基座与离散接触，重点是状态估计、落足、平衡、WBC/RL 与防跌倒
- **机械臂**：工作空间、奇异位形、IK、轨迹/力控制、碰撞和末端任务
- **自动驾驶**：高速非完整约束，重点是多传感器融合、动态目标预测、功能安全与实时性
- **飞行/水下**：六自由度运动、流体动力、能源约束，以及空中/水下通信和环境安全

### 0.3 选型与组合原则

- 先从任务、环境、载荷、速度、续航、精度、安全和成本确定形态，再分解后续九大领域
- 移动操作机器人需要同时处理全局移动、局部操作、基座—机械臂协同、控制权和整机稳定性
- 👉 详细物理机制、约束属性、优缺点与控制图谱：[机器人分类学与物理特性对比](./robotics/robot_types.md)

---

## 一、感知层（传感器与感知 - Perception Layer）

> 感知层跨越硬件物理边界：高维感知（视觉识别、点云）运行于**上位机**，高实时本体感知（IMU、编码器）运行于**下位机**。

### 1.1 环境感知 (Exteroception)

#### 1.1.1 视觉类 (Vision)
- 单目 / 双目相机
- 深度相机（RGB-D：RealSense、Kinect）
- 激光雷达（2D/3D LiDAR）
- 红外相机

#### 1.1.2 距离与测距 (Proximity)
- 超声波传感器
- 毫米波雷达（测距+测速，全天候）
- ToF 飞行时间传感器

#### 1.1.3 自动驾驶传感器方案
- **纯视觉**：多路相机 + 视觉 SLAM + BEV 感知
- **视觉+激光雷达**：相机 + LiDAR + 毫米波雷达多传感器融合
- **高精定位**：RTK-GPS + IMU + 轮速计组合导航

#### 1.1.4 环境状态 (Environmental)
- 温湿度、气压/高度计、气体传感器

### 1.2 本体感知 (Proprioception)

#### 1.2.1 位置与运动传感
- 编码器（增量式 / 绝对式）
- IMU（内置陀螺仪 + 加速度计）

#### 1.2.2 力与接触传感
- 六维力矩传感器（足端/腕部核心）
- 一维拉压传感器
- 触觉传感器 / 电子皮肤

#### 1.2.3 全局参考传感
- RTK-GPS / GNSS、UWB 室内定位、磁力计

### 1.3 语音与交互传感器

#### 1.3.1 语音全链路 (Voice Pipeline)
- 麦克风阵列 / USB 独立麦克风（物理远离风扇白噪）
- **VAD**（语音活动检测）：0.5s 防死等，单行极速刷新
- **ASR**（语音识别）：Faster-Whisper（本地离线）+ Gemini Live API（云端全双工）
- **TTS**（语音合成）：VITS 离线 + Edge-TTS 云端
- **全双工网关**：WebSocket 长连接 + 中断恢复
- 👉 专题：[语音全链路详解](./robotics/speech_pipeline.md)
- 👉 实战案例：[Gemini 全双工语音交互](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/21.3.gemini_model.md) · [本地大模型语音](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/21.2.local_AI_large_model.md)

### 1.4 高层感知算法【运行于：上位机】 👉 [AI与机器人学习笔记](./robotics/AI_learning_robotics.md) · [视觉基础模型 VFM 专题](./robotics/vision_foundation_models.md)

- **经典检测管线（工程主力）**：YOLOv8 / Detectron2 实时目标检测；OpenCV · RealSense SDK · Lidar SDK
- **3D 感知**：PointNet 点云特征；Depth Anything 单目深度（无 RGB-D 时补几何）
- **视觉基础模型 VFM（开放词表 / 零样本）** 👉 [VFM 专题笔记](./robotics/vision_foundation_models.md)
    - **分割**：SAM / SAM2（点框提示）；Grounded-SAM（文本→检测+分割）
    - **检测**：Grounding-DINO（语言指定物体）；DINO v2/v3（跨帧 correspondence）
    - **位姿**：FoundationPose（6D 物体位姿）；典型管线：Grounding-DINO → SAM → FoundationPose → IK
    - **对齐**：CLIP / SigLIP（图文共享空间，供 VLA / 检索条件策略）
- 👉 实战案例：[YOLOv8 真机部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.3.real_robot_yolo_environment.md) · [VLM 图像触发](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/30.AI_image_identification.md)

### 1.5 状态估计与世界表征（连接感知与规划控制的跨层桥梁） 👉 [状态估计专题](./robotics/state_estimation.md) · [传感器融合](./robotics/sensor_fusion.md) · [系统集成总骨架](./robotics/robot_system_integration.md#二抽象总骨架所有模式的总图)

> 原始传感数据不能直接等同于机器人状态。该模块先统一时间与坐标，再形成可供规划和控制使用的机器人状态与环境表征；高频本体估计通常靠近下位机，视觉定位、地图与语义表征通常运行于上位机，具体部署取决于平台实时性和算力。

#### 1.5.1 数据预处理、同步与标定
- **时钟同步**（硬件时间戳 / PTP / NTP）：跨传感器、跨主机数据对齐的前提
- **系统标定**：相机内参（张正友标定法）、手眼标定（$AX=XB$）、多传感器联合外参、IMU 零偏标定 👉 [相机模型与标定](./robotics/camera_calibration.md)
- **预处理**：去噪、滤波、异常值剔除、坐标变换与数据新鲜度检查

#### 1.5.2 机器人状态估计 (Robot State Estimation)
- **里程计推算**：利用运动学模型（轮式/腿部）推算位姿变化，作为高频里程计观测源
- **状态融合**：卡尔曼滤波 / EKF / UKF，融合 IMU + 关节里程计 + 视觉里程计（VIO）👉 [状态估计](./robotics/state_estimation.md) · [传感器融合](./robotics/sensor_fusion.md)
- **输出状态**：基座位姿/速度、关节状态、接触状态及估计不确定性，供规划器与控制器使用
- **双足/人形特有问题**：腿部里程计（接触检测 + 运动学推算）、浮动基座状态估计、触地判定（阈值依传感器和机型标定）

#### 1.5.3 环境与世界表征 (World Representation)
- **几何表征**：里程计、点云、占据栅格、2D/3D 地图
- **语义表征**：目标位姿、语义地图、场景图，为导航、抓取和任务规划提供统一世界状态
- **坐标关系**：通过 [TF 树](./robotics/tf_tree.md) 维护 `map → odom → base → sensor/ee` 的时空关系
- 👉 实战案例：[关节标定](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/26.joint_calibration.md)

---

## 二、应用、任务决策与规划（上位机 / “大脑” - Application, Task & Planning）

> 本领域回答四个递进问题：**上位机依靠什么算力运行**、**要完成什么应用**、**如何理解并编排任务**、**如何生成可执行的路径与轨迹**。上位机通常承载语义感知、任务规划和计算密集型算法，但具体部署取决于实时性、算力、功耗与平台架构；操作系统和 ROS 中间件作为上下位机共用的软件基础设施放在第九章。

### 2.1 上位机计算平台 (High-level Compute Platform)

#### 2.1.1 轻量级边缘计算
- 树莓派 / Rockchip RK3588
- 低功耗边缘计算盒
- **典型负载**：轻量视觉、语音交互、ROS 节点与简单任务逻辑

#### 2.1.2 大算力平台
- NVIDIA Jetson AGX Orin / Orin NX
- x86 高性能主机（Intel NUC i7/i9 等）
- 独立 GPU 工作站（本地大模型、VLA 训练或推理）
- **典型负载**：多路视觉、SLAM、MoveIt、VLA/LLM 与任务规划

#### 2.1.3 专用硬件加速
- FPGA、AI NPU/TPU
- 用于确定性预处理、视觉推理或特定算子加速；是否采用取决于功耗、时延和工具链

#### 2.1.4 外部开发主机与 micro-ROS
- **外部 PC/笔记本**：开发阶段可直接用个人电脑当上位机，通过以太网/WiFi 组网跑感知和规划节点，省去板载硬件
- **micro-ROS**：ROS 2 在 MCU（STM32/ESP32 等）上的轻量实现，让传感器和简单控制直接作为 ROS 2 节点运行

### 2.2 应用与人机交互 (Applications & HRI)

- **典型应用**：自主导航、视觉抓取、接触装配、巡检搬运、遥操作示教、具身交互与全身表演
- **显式交互**：语音指令、手柄/摇杆（H12 遥控器）、UI/Web 监控
- **隐式交互**：人脸识别与跟踪、手势识别、头部姿态跟随
- **全身表演动作**：太极、编舞、CSV 动作序列重放
- 👉 实战案例：[人脸识别](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/32.1.face_recognition.md) · [人脸跟踪融合](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/32.2.face_recognition_traking.md) · [头身协同视觉跟随](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/24.1.visual_tracking.md) · [H12 遥控器](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/17.h12_remote_control.md) · [太极全身动作](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/10.Tai_Ji.md) · [手臂编舞](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/13.arm_move.md) · [机器人舞蹈](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/14.robot_dance.md)

#### 2.2.1 数据采集与遥操作 (Data Collection) 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md) · [AI/VLA 数据工程](./robotics/ai_vla_data_engineering.md)

- **自采（实战案例）**：LeRobot v3.0 格式（observation 图像+关节状态 + action），三机分工（下位机录 npz + 上位机录 RGB + PC 离线打包），单条 episode ~1200 帧 @50Hz
- **公开采集范式**：ALOHA 主从双臂遥操作 · UMI 可穿戴 retargeting · Ego-centric 第一人称视频（低成本、弱 action 标注）
- **公开大规模 Dataset（训通用 VLA/IL）** 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)
    - [Open X-Embodiment (RT-X)](https://robotics-transformer-x.github.io/) · [DROID](https://droid-dataset.github.io/) · [BridgeData V2](https://rail-berkeley.github.io/bridgedata/) · [AgiBot World](https://agibot-world.com/)
    - 数据扩增：[MimicGen](https://github.com/NVlabs/mimicgen) · [RoboTwin 2.0 合成](https://github.com/robotwin-Platform/robotwin)
- 动捕系统（OptiTrack / Vicon）· VR 遥操作（Apple Vision Pro / Meta Quest）· rosbag2 多模态录制
- 👉 实战案例：[LeRobot 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) · [相机/动捕](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/27.camera_mtion_capture.md)

#### 2.2.2 AI/VLA 数据闭环 👉 [AI、VLA 与数据工程专题](./robotics/ai_vla_data_engineering.md)

- **数据闭环**：采集契约与时间同步 → 清洗/标注/质量检查 → 数据版本与血缘 → 防泄漏划分 → 困难样本回流
- **模型生命周期**：可复现训练与实验追踪 → 离线/仿真/真机分层评测 → 模型制品与兼容校验 → 灰度发布/回滚
- **VLA 运行时约束**：技能/动作接口、多速率执行、动作有效期、控制权与安全过滤、前后置条件和失败恢复
- **可观测性**：输入质量、推理 P95/P99、动作拒绝率、任务成功/接管/安全触发率，以及模型/数据/标定/本体版本追踪

### 2.3 任务理解、技能编排与智能决策 (Task & Skill Orchestration)

#### 2.3.1 具身智能与 VLA (Embodied AI / VLA) 👉 [VLA 研究版图](./robotics/vla_landscape.md) · [AI/VLA 工程闭环](./robotics/ai_vla_data_engineering.md)

- **两条路线**：研究型**端到端 VLA**（OpenVLA/Octo/π0） vs **工程分层 VLA**（System 2 规划 + System 1 检测/IL + IK/WBC）👉 [专题流程图](./robotics/vla_landscape.md)
- **System 2 编排形态**：状态机 → [行为树](./robotics/ros_logic.md) → MCP / Tool Call（同一抓取链，三种高层接口）
- **研究侧版图**：RT-1/2 · OpenVLA · Octo · π0 · 2025 分层双系统（Hi-Robot · GR00T-N1 · GO-1）· 人形 NaVILA / RDT-1B
- **模仿学习 System 1 基线**：ACT / Diffusion Policy / DP3；脑体分离（训练 PyTorch + 部署 [Docker](./robotics/docker.md) [ROS](./robotics/ros_logic.md)）
- **深度学习基础设施**：PyTorch / [TensorRT / ONNX Runtime](./robotics/edge_deployment.md)
- **工程落地**：VLA 不直接绕过任务编排与安全层；模型包同时携带预处理、归一化、I/O/关节映射、兼容矩阵和评测证据 👉 [专题](./robotics/ai_vla_data_engineering.md)
- 👉 **实战案例**：[22.1–22.4 VLA 系列](https://github.com/651yyds3939/kuavo-dev-notes/tree/master/kuavo_notes) · [完整索引见专题文末](./robotics/vla_landscape.md#实战案例索引-kuavo-dev-notes)

#### 2.3.2 任务编排与逻辑调度

- **行为树 (Behavior Trees)**：py_trees，行为封装为独立节点，可组合/替换/插入，解决千行 if-else 状态机维护难题 👉 架构见 [ROS 架构逻辑](./robotics/ros_logic.md)
- 状态机 (State Machine)
- **AI Agent 工作流**：LangChain / CrewAI / n8n
- 👉 实战案例：[行为树版 VLA 抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md)

#### 2.3.3 LLM for Robotics（高层规划与工具调用） 👉 [LLM for Robotics 专题](./robotics/llm_for_robotics.md)

- **定位**：LLM 通常**不直接输出关节角**，而是做任务理解、分解、规划与 Tool Call（~1Hz System 2），低层交给 VLA / 行为树 / MoveIt
- **部署路线（通用）** 👉 [专题笔记](./robotics/llm_for_robotics.md)：本地耳脑嘴三分离 · 云端全双工 · 视觉/VLM 触发 · 语音意图+操作 · MCP Agent · 认脸/跟随交互
- **研究范式**：PaLM-E · LLM+P · VoxPoser · Code as Policy · [Embodied Agent Interface](https://embodied-agent-interface.github.io/)
- **工程编排形态**：状态机 · 行为树 · MCP/Tool Call（见专题 §5–§7 流程图）
- 👉 **实战案例**：[21.2 本地语音](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/21.2.local_AI_large_model.md) · [21.3 云端全双工](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/21.3.gemini_model.md) · [22.3 MCP](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md) · [32.1/32.2 认脸交互](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/32.1.face_recognition.md) · [完整索引见专题文末](./robotics/llm_for_robotics.md#实战案例索引-kuavo-dev-notes)

### 2.4 空间与运动规划 (Spatial & Motion Planning)

#### 2.4.1 导航与建图 (Navigation & SLAM) 👉 [SLAM 专题](./robotics/slam.md) · [路径规划](./robotics/path_planning.md)
- ROS Navigation / Nav2（轮式全栈路径规划与避障）
- **SLAM**：2D/3D 激光（Cartographer/FAST-LIO）、V-SLAM（ORB-SLAM3）、回环检测、图优化
- **路径规划算法**：全局：A* / RRT* / PRM；局部：DWA / TEB / MPC 👉 详见 [路径规划专题](./robotics/path_planning.md)
- [FAST-LIO（LiDAR 里程计）](./robotics/slam.md)、[Docker 挂载](./robotics/docker.md) 踩坑
- 👉 实战案例：[地图导航与 FAST_LIO](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/3.map_navigation.md) · [官方导航集成](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/3.1official_navigation.md)

#### 2.4.2 机械臂与运动规划 (Manipulation) 👉 [MoveIt 专题](./robotics/moveit_manipulation.md) · [经典动力学与运动控制](./robotics/dynamics_control.md)

- ROS MoveIt / MoveIt 2（运动规划、碰撞检测、[逆运动学](./robotics/dynamics_control.md)）
- IK 求解器：TRAC-IK（冗余自由度优化求解）
- OctoMap 3D 点云避障 + OMPL 路径规划
- **视觉抓取管线**：YOLO → TF2 坐标变换 → IK 逆解 → 轨迹生成 → 抓取执行
- **轨迹生成 (Trajectory Generation)**：最小 jerk / 最小 snap 平滑、B-spline / 五次多项式插值、时间参数化（Time-parameterization）、Via-points → 连续轨迹
- **抓取理论基础**：力封闭（Force Closure）/ 形封闭（Form Closure）、摩擦锥（Friction Cone）、抓取质量度量
- 👉 实战案例：[MoveIt 经典版/OctoMap 双轨抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/28.moveit_grasping.md) · [IK 逆运动学](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/9.IK.md) · [TF2 视觉抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.4real_visual_grasp.md) · [视觉抓取基础](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/6.visual_grasp.md)

---

## 三、控制层（下位机 / “小脑” - Motion Control）

> 下位机负责"怎么动得稳"。在双足人形中，它是运行实时 OS 的高性能主机，负责 1kHz 动力学控制与安全兜底。
>
> **多速率控制架构**（典型人形案例，频率依平台而异）：高频伺服/全身控制通常运行于数百 Hz–1kHz；MPC 常以数十至数百 Hz 更新优化结果；[RL](./robotics/RL.md) 策略可在约 50Hz 推理（[ONNX](./robotics/edge_deployment.md)）；视觉常在约 30Hz；大模型异步运行。层间通过带时间戳的目标、低通滤波与插值平滑衔接，避免阶跃冲击。

### 3.1 控制硬件

#### 3.1.1 经典 MCU（轮式/普通机器人）
- ARM Cortex-M（STM32）、ESP32、Arduino

#### 3.1.2 高性能 PC 级（人形/多足机器人）
- x86 高性能主机（胸部 NUC），充当 ROS Master
- 工业 PLC / 多轴运动控制卡

### 3.2 操作系统与通信

#### 3.2.1 实时操作系统
- PREEMPT_RT（Linux 实时补丁；常用于对确定性有要求的高频控制平台，并非所有机器人都必须采用）
- FreeRTOS / RT-Thread（MCU 级）
- VxWorks（商用高可靠）

#### 3.2.2 高速总线主站
- EtherCAT 主站（微秒级同步，全身几十个关节高频下发） 👉 [现场总线与 EtherCAT 专题](./robotics/fieldbus_and_ethercat.md)
- CAN / CAN FD 主站

### 3.3 核心控制算法

#### 3.3.1 经典闭环控制 👉 [PID 控制专题](./robotics/pid_control.md)
- 独立关节 PID 控制律（P/I/D 三项 + 前馈）
- **级联控制**：电流环（20-100kHz）→ 速度环（1-5kHz）→ 位置环（100-1000Hz）
- **前馈控制**：[逆动力学前馈](./robotics/dynamics_control.md) + [PID](./robotics/pid_control.md) 反馈 = 零延迟 + 误差纠正
- 底盘运动学逆解（差速、全向轮）
- 抗积分饱和（Anti-windup）、低通滤波降噪

#### 3.3.2 高阶动力学与平衡控制 👉 [经典动力学与运动控制](./robotics/dynamics_control.md)
- **[全身控制 (WBC)](./robotics/dynamics_control.md)**：多任务层级优化，同时满足姿态/平衡/操作
- **逆运动学 (IK)**：雅可比矩阵 $J$，速度映射 $\dot{x}=J\dot{q}$，静力映射 $\tau=J^T F$；冗余自由度通过零空间投影 (Null-space Projection) 在完成主任务的同时优化次要目标（避关节限位、避奇异等）
- **[模型预测控制 (MPC)](./robotics/dynamics_control.md)**：有限时域优化
- **ZMP** 动态平衡 / 质心规划 / 奇异点规避
- **阻抗/导纳控制** 👉 [阻抗控制专题](./robotics/impedance_control.md)：虚拟弹簧-阻尼-质量模型，刚度/阻尼参数调优，柔顺交互物理底座
- **双足平衡与抗扰动**：踝策略 → 髋策略 → 迈步策略（分级推恢复）、捕获点（Capture Point）理论
- **CoT (Cost of Transport)**：单位质量单位距离的能量消耗，衡量移动效率的核心指标
- **示教与重力补偿**：拖动示教 + 零力矩模式
- 👉 实战案例：[示教/重力补偿](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/18.teaching_gravity_compensation.md) · [上下楼梯仿真](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/5.up_down_stair.md)
- 👉 理论基础：[优化理论（QP/NLP在控制中的作用）](./robotics/optimization_theory.md)

#### 3.3.3 数据驱动运动控制 (Data-Driven Locomotion) 👉 [RL 笔记](./robotics/RL.md) · [世界模型详解](./robotics/world_model.md)

- **PPO 强化学习行走**：[Isaac Lab](./robotics/RL.md) 训练，87维 obs 跟踪 $(v_x, v_y, \omega)$，[ONNX 导出](./robotics/edge_deployment.md) → [MuJoCo Sim2Sim](./robotics/robot_modeling.md) → 真机部署
- **IL+RL 全身舞蹈**：CSV 动作参考轨迹 + mimic 跟踪奖励，115维 obs，4096 并行环境（8GB 显存）
- **TD-MPC2 世界模型**：隐式世界模型 + MPPI 规划，对比 model-based RL vs PPO 的样本效率
- **训练技巧**：课程学习（由易到难逐步增加任务复杂度）、奖励塑形（Reward Shaping，引入辅助奖励引导策略收敛）
- **混合级联架构**（现代人形常见方案之一）：[RL](./robotics/RL.md) 生成动作/姿态参考 → [MPC](./robotics/dynamics_control.md) 以较低频率优化预测轨迹（可选）→ 高频 [WBC](./robotics/dynamics_control.md) / 伺服控制满足动力学约束并执行安全限制；具体分工与频率依平台而异
- **Sim2Real 核心痛点**：S49 机型 [URDF](./robotics/robot_modeling.md) 与训练资产版本撕裂，需手动缝合 `.info` 与 `humanoidController.cpp`；[ONNX](./robotics/edge_deployment.md) 观测空间对齐（CSV 关节顺序必须 100% 一致）
- 👉 实战案例：[RL 行走 Sim2Real 真机部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) · [奖励函数/域随机化拆解](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.2RL_lab_analysis_code.md) · [IL+RL 舞蹈总览](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.1.RL_dance_overview.md) · [S49 舞蹈训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.3.RL_dance_train.md) · [TD-MPC2 世界模型](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/31.1.world_model.md)

---

## 四、执行层（执行器 / “肌肉与神经末梢” - Actuators）👉 [硬件与整机工程专题](./robotics/hardware_system_engineering.md)

### 4.1 驱动级控制 👉 [FOC 矢量控制](./robotics/motor_foc.md)
- 关节级 MCU（内嵌伺服驱动板）
- **FOC 矢量控制**：Clarke/Park 变换、SVPWM、转矩/励磁解耦（$I_q$ 控力矩，$I_d$ 控磁场）
- 电流环 → 速度环 → 位置环（三环级联，内环频率 5-10× 外环）
- 功率变换电路（MOSFET/IGBT 逆变桥）

### 4.2 运动执行器与选型
- 高扭矩无框力矩电机（人形关节常用）· BLDC / PMSM / 伺服电机
- 直线电机 / 电动推杆 / 滚珠丝杠
- **关键指标**：连续/峰值力矩与速度、峰值持续时间、效率、热容量、质量和控制带宽

### 4.3 传动与关节模组
- 谐波 / RV / 行星减速器、同步带 / 绳驱：联合权衡减速比、效率、回差、刚度、背驱性和冲击寿命
- **背驱性 (Backdrivability)**：输出端受力时能否反向驱动输入端——高背驱性关节能实现柔顺交互和被动抗冲击，是人形安全的关键指标
- 一体化关节：电机 + 减速器 + 轴承 + 编码器 + 驱动器 + 温度检测
- **模组保护**：位置/速度/力矩/电流/温度限值、机械限位与制动器；失电响应需按整机风险设计

### 4.4 末端执行器
- 灵巧手（多指独立驱动）/ 平行夹爪 / 柔性抓取器 / 真空吸盘
- 👉 实战案例：[夹爪安全与硬件调试](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/20.gripper_issue.md)

### 4.5 关节标定、热与维护
- 编码器零位、传动方向/减速比、摩擦、刚度与阻尼标定
- 温升、润滑、回差、噪声和寿命监测；模组更换后同步恢复参数与版本
- 👉 实战案例：[关节标定](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/26.joint_calibration.md) · [官方包升级与排障](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/25.update.md)

---

## 五、机械结构与整机工程 (Mechanical & Hardware System) 👉 [硬件与整机工程专题](./robotics/hardware_system_engineering.md) · [机器人建模](./robotics/robot_modeling.md) · [研发全流程](./robot_development_lifecycle.md)

> 结构、执行器、电源、线束和热设计必须围绕整机指标联合闭环，而不是独立选型后再拼装。

### 5.1 形态、自由度与总体布局 👉 [机器人分类与特性对比](./robotics/robot_types.md)
- 轮式 / 履带式 / 双足 / 四足 / 固定或移动机械臂
- 自由度、工作空间、负载、稳定性、质量分布、传感器视场和线束路径联合设计

### 5.2 机械→软件建模管线 (CAD-to-URDF Pipeline)
- **3D 建模**：SolidWorks / Fusion 360 零件建模 → 装配体 → 工程图
- **制造**：3D 打印（快速原型）· CNC 加工（金属结构件）· 碳纤维板材切割
- **导出 URDF**：SolidWorks URDF Exporter 插件 / `sw2urdf` → 生成 ROS 可用的机器人模型 👉 [机器人建模专题](./robotics/robot_modeling.md)
- **管线闭环**：CAD 修改 → 重新导出 URDF/MJCF → 更新仿真资产 → 控制参数同步

### 5.3 骨架、外壳与结构验证
- 航空铝合金、钢、镁合金、工程塑料、碳纤维等按强度/刚度/疲劳/加工与成本选材
- 静强度、刚度、模态、疲劳和冲击分析；主要结构模态应与控制带宽协同评估
- 外壳兼顾碰撞防护、散热、传感器视场、夹点消除与维修拆装

### 5.4 传动、轴承与装配工程
- 同步带 / 齿轮齿条 / 连杆 / 钢丝绳传动；轴承、联轴器、密封和减震
- 公差链、轴系同轴度、轴承预紧、螺栓力矩、防松、润滑与装配基准

### 5.5 整机预算与多物理耦合
- **预算闭环**：质量/重心/惯量、连续/峰值力矩、功率/续航、热、结构余量、空间和成本
- **数字一致性**：CAD/BOM ↔ URDF/MJCF ↔ 控制参数 ↔ 标定 ↔ 仿真/训练资产

### 5.6 样机集成、制造与质量
- 分级 Bring-up：不上电检查 → 低压通信 → 单驱动/单关节 → 子组件 → 受保护整机 → 额定工况
- DFM/DFA/DFT、线束与连接器防错、关键尺寸/紧固力矩/序列号追溯、来料/过程/出厂检验
- 👉 详细选型权衡、预算、热/EMC、验证矩阵与检查表：[机器人硬件与整机工程](./robotics/hardware_system_engineering.md)

---

## 六、安全工程 (Safety Engineering) 👉 [安全工程专题](./robotics/safety_engineering.md) · [真机调试 SOP](./robotics/safety_sop.md)

> 安全不是单一急停或操作注意事项，而是贯穿**危险识别 → 安全需求 → 分层防护 → 验证证据 → 运行反馈**的生命周期工程；SOP 只是其中一层。

### 6.1 危险分析与安全需求
- 识别机械、电气、热、电池、控制、通信和人因危险，将危险追溯到可验证的安全需求与残余风险

### 6.2 分层防护与安全状态
- 优先顺序：本质安全设计 → 工程防护 → 信息/培训/SOP
- 安全状态：正常 → 能力受限 → 受控停止 → 制动 → 切断动力（不能一律锁死或断电）

### 6.3 功能安全与故障响应
- 指令校验（新鲜度/范围/变化率/坐标对齐）、看门狗、故障检测与隔离 (FDIR)
- AI/RL 输出受低层可行性、限幅和独立安全监控约束

### 6.4 安全验证与变更管理
- MIL/SIL/HIL 逐级验证、故障注入、响应时间/停止距离记录
- 硬件、模型、参数或场景变化后重新评估

### 6.5 真机调试安全
- 龙门架/防坠、隔离区、低速低能量、双人操作、急停和模式切换
- 👉 详细方法、验证矩阵与检查表：[机器人安全工程](./robotics/safety_engineering.md) · 实机操作步骤：[真机安全 SOP](./robotics/safety_sop.md)

---

## 七、通信系统 (Communication) 👉 [ROS 通信原理详解](./robotics/ros_communication.md)

### 7.1 内部总线与网络

#### 7.1.1 高速硬实时总线（小脑 ↔ 全身关节）
- EtherCAT（微秒级同步，链型拓扑）
- CAN / CAN FD（毫秒级同步）

#### 7.1.2 板级与外设
- UART / USB / SPI / I2C

#### 7.1.3 大脑与小脑通信（上位机 ↔ 下位机） 👉 [ROS 通信原理](./robotics/ros_communication.md) · [TF 树笔记](./robotics/tf_tree.md)

- **物理连接**：内部千兆以太网（机身骨架集成）+ 静态 IP 局域网（下位机 `.1`，上位机 `.12`）
- **组网铁律**：`ROS_MASTER_URI` 绑定下位机、各自暴露 `ROS_IP`、物理网线直连禁用 WiFi 传控
- **跨机权限隔离**：运动节点 `root`（EtherCAT）· 逻辑节点 `lab`（防 root 污染）· 视觉/语音节点 `leju_kuavo`
- **故障模式**：网络闪断 → 下位机按风险等级进入保活/受控停止/制动；上位机死机 → 下位机独立维持安全状态
- **传输选择**：控制指令优先低延迟（UDP/DDS），配置文件优先可靠到达（TCP）
- **核心数据流**：上位机下发视觉目标姿态 + 任务指令 → 下位机回传底盘状态 + 硬件报警
- 👉 实战案例：[上下位机网络配置](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/16.Internet.md)

#### 7.1.4 ROS 应用层通信（Topic / Service / Action） 👉 [ROS 通信原理](./robotics/ros_communication.md)
- **Topic（话题）**：发布/订阅，异步单向，多对多。适用高频连续数据流（传感器、`/cmd_vel`、`/joint_states`）
- **Service（服务）**：请求/响应，同步阻塞，一对多。适用瞬时指令（标定、复位、夹爪控制）
- **Action（动作）**：带反馈和取消的长周期任务。适用抓取、导航等可能耗时几十秒的操作
- **TF 坐标变换**：维护 `map → odom → base → sensor/ee` 的实时坐标树 👉 [TF 树笔记](./robotics/tf_tree.md)
- 中间件架构与开发环境见 👉 [§9.1 操作系统与机器人中间件](#91-操作系统与机器人中间件)

### 7.2 外部遥测与交互
- Wi-Fi（局域网 SSH 调试）、Bluetooth（手柄接入）
- 4G/5G 蜂窝网络（云端大模型 API 接入）

---

## 八、电源与配电系统 (Power & Distribution) 👉 [硬件与整机工程专题](./robotics/hardware_system_engineering.md#五电气电源与线束)

### 8.1 电池与能量预算
- 高倍率动力电池组：按任务循环核算可用能量、持续/峰值放电、老化降额、机械固定和热风险
- BMS：电芯均衡、SOC/SOH、温度/电流/绝缘监测与充放电保护

### 8.2 电源转换、分配与保护
- 主接触器/预充/熔断器、PDU、多路 DC-DC；动力域、逻辑域和安全域按架构隔离
- 校核峰值电流、母线压降/纹波、再生能量、上电/掉电/充电时序、短路与接反故障

### 8.3 线束、热与 EMC
- 线径/压降、屏蔽/双绞/接地、最小弯曲半径、应力释放、连接器防呆与插拔寿命
- 电池/驱动/计算平台热路径和降额；动力线与编码器/通信分区，验证 ESD、EFT、浪涌和电压跌落

---

## 九、系统软件与开发、测试和工程化环境 (System Software & DevOps) 👉 [环境相关笔记](./robotics/environment.md)

> 操作系统和机器人中间件是感知、规划与控制共同依赖的软件基础设施；上位机计算硬件见第二章，下位机实时控制硬件见第三章。
>
> 👉 从零部署：[仿真/实机环境部署全流程](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/1.start.md) · [第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)

### 9.1 操作系统与机器人中间件
- Ubuntu / Debian（通用 Linux）· Yocto（定制嵌入式 Linux）
- **ROS 1（Noetic）**：Master 负责节点注册与发现；节点建立连接后通常通过 TCPROS/UDPROS 直接交换数据
- **ROS 2（Humble/Iron 等）**：基于 DDS 的分布式发现与通信，通过 QoS 配置可靠性、历史、截止期限和存活性
- `ros2_control`：硬件抽象与控制器管理框架，支持真实硬件与仿真后端复用
- 👉 入门模板：[ROS2 最小工作空间](./robotics/ros_code_template/ros2_code_ws/) · [ROS1 工作空间](./robotics/ros_code_template/ros1_code_ws/) · [工作空间文件速查](./robotics/doc_concept.md)

### 9.2 仿真与 Sim-to-Real 👉 [RL 笔记](./robotics/RL.md) · [环境笔记](./robotics/environment.md) · [模型部署](./robotics/edge_deployment.md) · [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)

- **[MuJoCo](./robotics/robot_modeling.md)**：轻量级动力学，大规模 RL 训练首选
- **Isaac Sim / Isaac Lab**：GPU 并行 + 光线追踪渲染，视觉模型与 Sim2Real 核心工具
- **Gazebo**：经典 ROS 移动机器人仿真环境
- **域随机化**：质量/摩擦/延迟随机噪声注入，Sim2Real 跨越虚实鸿沟的核心武器；其他迁移路线：域自适应 (Domain Adaptation)、系统辨识 (System ID)、在线自适应
- 👉 实战案例：[Isaac Lab 行走训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md) · [MuJoCo Sim2Sim](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.3RL_lab_sim_to_sim.md)

#### 9.2.1 评测基准与公开数据集 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)

> 仿真器决定「能造什么世界」；**Benchmark** 决定「怎么比」；**Dataset** 决定「学到什么分布」。

- **操作 Benchmark**：RoboTwin 2.0 · LIBERO · CALVIN · Meta-World · SimplerENV
- **规划 Benchmark**：Embodied Agent Interface（LLM 决策链评估）
- **跨本体 Dataset**：Open X-Embodiment · DROID · BridgeData V2 · 白虎/青龙

### 9.3 开发工具与调试

- **AI 辅助开发**：Claude Code / Cursor（跨文件重构、架构咨询）· VS Code + GitHub Copilot 👉 [Claude Code 配置](./ubuntu/claude_code_deepseek.md) · [Cursor 使用](./ubuntu/cursor.md)
- **调试与可视化**：RViz · PlotJuggler · Foxglove Studio · rqt_console · rosbag 👉 [抖动 rosbag 排障](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/19.tremble_rosbag.md)
- **性能分析**：NVIDIA Nsight（CUDA 与渲染）
- 👉 工具链：[终端命令速查](./robotics/terminal_command.md) · [终端工具](./ubuntu/Terminal_tools.md) · [Conda 环境管理](./ubuntu/conda.md) · [具身智能工程工具箱](./robotics/tools.md)

### 9.4 容器化与版本控制 👉 [Docker 笔记](./robotics/docker.md) · [Git/GitHub 笔记](./robotics/git_github.md)

- **Docker**：容器化部署，Namespace 隔离 + Cgroups 限流，Volume 挂载 👉 [Docker 全生命周期 + 午夜排雷案例](./robotics/robotics_architecture_master_guide.md)
- **Git**：工作区/暂存区/本地仓库三层架构，子模块指针机制，`git stash -u` 保护魔改笔记 👉 [Git 拉取与子模块](./robotics/git_pull.md)

### 9.5 C++ 工程化与代码模板

- **C++ 工程化**（读/写机器人底层源码）👉 [Linux C++ 工业级项目方向](./robotics/linux_C++_project.md) · [机器人底层 C++ 指南](./robotics/code/robotics_C++.md) · [C++ 语法补充](./robotics/code/C++_grammar_supplement.md) · [DSA 基础](./robotics/code/DSA_C++_Basics.md) · [DSA 树专题](./robotics/code/DSA_tree.md) · [机器人岗位技能对照](./robotics/code/Job_Requirements_for_Robot.md)
- **ROS 代码模板**：[ROS2 最小工作空间](./robotics/ros_code_template/ros2_code_ws/) · [ROS1 工作空间](./robotics/ros_code_template/ros1_code_ws/) 👉 [工作空间文件速查](./robotics/doc_concept.md)
- **代码阅读**：[代码阅读技巧](./robotics/code_read_skill.md)

### 9.6 CI/CD 与系统工程 👉 [系统工程专题](./robotics/systems_engineering.md) · [系统集成笔记](./robotics/robot_system_integration.md)

- **CI/CD**：GitHub Actions / GitLab CI（自动构建 + 仿真测试管道）
- **系统工程**：需求与接口、系统预算、风险与降级、质量闭环、运维与安全
- 👉 详细方法、交付物与检查表：[机器人系统工程与全生命周期质量](./robotics/systems_engineering.md)

### 9.7 文档与项目管理
- Markdown 结构化文档 + Mermaid 架构图
- **核心文档**：需求基线、架构说明、ICD、预算/风险表、V&V 矩阵、兼容性矩阵、发布说明和运维手册
- 👉 研发全流程（时间/流程视角）：[robot_development_lifecycle.md](./robot_development_lifecycle.md) · 运行时闭环：[robot_system_integration.md](./robotics/robot_system_integration.md)
- 👉 实战：[54 篇人形机器人二次开发文档](https://github.com/651yyds3939/kuavo-dev-notes) · [SDK 接口速查](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/%E6%8E%A5%E5%8F%A3%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3.md) · [资源链接汇总](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/999kuavo_resource.md)

---

> **备注**：领域结构视角（本文件）与 [研发全流程](./robot_development_lifecycle.md)（时间视角）互补——前者回答「由什么组成」，后者回答「如何被造出来」；运行时严格的数据流与控制流见 [系统集成](./robotics/robot_system_integration.md)。
>
> 这份思维导图不是一次写成的，而是在不断学习中完善的，也经历了很多次实机调试、炸机排障和架构重构后逐层沉淀下来的。每一层背后都有至少一篇实战笔记支撑。
>
> 通用知识库：[robotics-notes](https://github.com/651yyds3939/robotics-notes) · 项目实战：[kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)
