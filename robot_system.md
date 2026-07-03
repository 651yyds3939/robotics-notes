# 机器人全链路系统 (Full-Stack Robotics System)

> **使用说明**（与 [README.md](./README.md) 一致）
>
> 本文件是**机器人全链路系统**的主索引，按九大层组织：感知 → 决策 → 控制 → 执行 → 通信 → 工程化。导图内已加入可点击链接：
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
> **HTML 离线版提示**（详见过 [README「用浏览器打开 HTML 版」](./README.md#用浏览器打开-html-版离线)）：
> - 终端：`xdg-open /path/to/robotics-notes/robot_system_photo.html`（将路径改为本机实际目录）
> - 须从 **`robotics-notes/` 仓库根目录内**打开，勿单独拷贝 HTML，否则 `assets/markmap/` 会失效
> - 若主区域空白、仅见右下角工具栏：点 **「适应屏幕」**，或 `Ctrl + Shift + R` 刷新
> - 修改本 `.md` 后运行 `./regenerate_robot_system_html.sh` 可更新 HTML；完全同步仍推荐 **Markmap 直接打开本文件**
>
> 📂 **GitHub**：[robotics-notes](https://github.com/651yyds3939/robotics-notes)（本库 · 通用理论/架构/工具链）· [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（Kuavo 4 Pro 实机/仿真二次开发，54 篇实战文档）
>
> 💡 不同形态机器人 👉 [机器人分类与特性对比](./robotics/robot_types.md)

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
- ToF 飞行时间传感器

#### 1.1.3 环境状态 (Environmental)
- 温湿度、气压/高度计、气体传感器

### 1.2 本体感知 (Proprioception)

#### 1.2.1 运动学
- 编码器（增量式 / 绝对式）
- IMU（惯性测量单元）、陀螺仪、加速度计

#### 1.2.2 动力学
- 六维力矩传感器（足端/腕部核心）
- 一维拉压传感器
- 触觉传感器 / 电子皮肤

#### 1.2.3 全局定位
- RTK-GPS / GNSS、UWB 室内定位、磁力计

### 1.3 语音与交互传感器

#### 1.3.1 语音全链路 (Voice Pipeline)
- 麦克风阵列 / USB 独立麦克风（物理远离风扇白噪）
- **VAD**（语音活动检测）：0.5s 防死等，单行极速刷新
- **ASR**（语音识别）：Faster-Whisper（本地离线）+ Gemini Live API（云端全双工）
- **TTS**（语音合成）：VITS 离线 + Edge-TTS 云端
- **全双工网关**：WebSocket 长连接 + 中断恢复
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

### 1.5 底层状态估计与预处理【运行于：下位机】 👉 [状态估计专题](./robotics/state_estimation.md) · [传感器融合](./robotics/sensor_fusion.md)

- **时钟同步**（PTP / NTP）：多传感器高频数据对齐前提
- **系统标定**：相机内参（张正友标定法）、手眼标定（$AX=XB$）、多传感器联合外参、IMU 零偏标定 👉 [相机模型与标定](./robotics/camera_calibration.md)
- **状态融合**：卡尔曼滤波 / EKF / UKF，融合 IMU + 关节里程计 + 视觉里程计（VIO）👉 [状态估计](./robotics/state_estimation.md) · [传感器融合](./robotics/sensor_fusion.md)
- **双足/人形特有问题**：腿部里程计（接触检测 + 运动学推算）、浮动基座状态估计、触地判定（20N 阈值）
- 👉 实战案例：[关节标定](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/26.joint_calibration.md)

### 1.6 数据采集与遥操作 (Data Collection) 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)

- **自采（Kuavo 实战）**：LeRobot v3.0 格式（observation 图像+关节状态 + action），三机分工（下位机录 npz + 上位机录 RGB + PC 离线打包），单条 episode ~1200 帧 @50Hz
- **公开采集范式**：ALOHA 主从双臂遥操作 · UMI 可穿戴 retargeting · Ego-centric 第一人称视频（低成本、弱 action 标注）
- **公开大规模 Dataset（训通用 VLA/IL）** 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)
 - [Open X-Embodiment (RT-X)](https://robotics-transformer-x.github.io/) · [DROID](https://droid-dataset.github.io/) · [BridgeData V2](https://rail-berkeley.github.io/bridgedata/) · [AgiBot World](https://agibot-world.com/)
 - 数据扩增：[MimicGen](https://github.com/NVlabs/mimicgen) · [RoboTwin 2.0 合成](https://github.com/robotwin-Platform/robotwin)
- 动捕系统（OptiTrack / Vicon）· VR 遥操作（Apple Vision Pro / Meta Quest）· rosbag2 多模态录制
- 👉 实战案例：[LeRobot 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) · [相机/动捕](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/27.camera_mtion_capture.md)

---

## 二、决策层（上位机 / “大脑” - High-level Decision）

> 上位机负责"看懂了什么"和"想干什么"。在人形机器人中，它是深度视觉、大语言模型和任务规划的运行载体。

### 2.1 计算硬件

#### 2.1.1 轻量级（轮式/普通机器人）
- 树莓派 / Rockchip RK3588
- 低功耗边缘计算盒

#### 2.1.2 大算力（人形/具身智能）
- Nvidia Jetson AGX Orin / Orin NX
- x86 高性能主机（Intel NUC i7/i9）
- 独立 GPU 工作站（本地大模型推理）

#### 2.1.3 硬件加速
- FPGA、AI NPU/TPU

### 2.2 操作系统与中间件 👉 [ROS 通信原理](./robotics/ros_communication.md) · [ROS2 开发流程](./robotics/ros2_process.md) · [ROS 架构逻辑](./robotics/ros_logic.md)

#### 2.2.1 操作系统
- Ubuntu / Debian（Linux 核心）
- Yocto（定制嵌入式 Linux）

#### 2.2.2 机器人中间件
- ROS 1（Noetic - 主从节点 TCP/IP 机制）
- ROS 2（Humble/Iron - DDS 去中心化通信）
- `ros2_control`：硬件抽象层，统一管理真实硬件与仿真切换
- 👉 入门模板：[ROS2 最小工作空间](./robotics/ros_code_template/ros2_code_ws/) · [ROS1 工作空间](./robotics/ros_code_template/ros1_code_ws/) · [工作空间文件速查](./robotics/doc_concept.md)

### 2.3 核心算法与框架

#### 2.3.1 具身智能与 VLA (Embodied AI / VLA) 👉 [VLA 研究版图专题](./robotics/vla_landscape.md)

- **Kuavo 工程 VLA 迭代（System 2 + System 1 分层）**：
 - V1 → ASR + LLM 意图提取 → JSON 指令 → 硬编码状态机执行（9 终端）
 - V2 → py_trees [行为树](./robotics/ros_logic.md) 重构（行为封装为独立节点，可组合替换）👉 实战见 [行为树版 VLA](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md)
 - V3 → MCP Tool Call（LLM 直接调用 `detect/grasp/speak` 函数，自主编排调用链）
- **研究侧 VLA 版图（视觉+语言→动作）** 👉 [VLA 研究版图专题](./robotics/vla_landscape.md)
 - 经典：[RT-1/2](https://arxiv.org/abs/2307.15818) · [OpenVLA](https://github.com/openvla) · [Octo](https://github.com/octo-models/octo) · [π0 / openpi](https://github.com/Physical-Intelligence/openpi)
 - 2025 分层双系统：System 2（VLM 规划）+ System 1（VLA 执行）—— [Hi-Robot](https://arxiv.org/abs/2502.19417) · [GR00T-N1](https://github.com/NVIDIA/Isaac-GR00T) · [GO-1 智元](https://www.zhiyuan-robot.com/)
 - 人形相关：[NaVILA](https://navila-bot.github.io/)（腿式+语言导航）· [RDT-1B](https://github.com/thu-ml/RoboticsDiffusionTransformer)（双臂）
- **模仿学习 System 1 基线**：ACT / Diffusion Policy / DP3，视觉→动作映射；脑体分离（大脑 PyTorch + 身体 [Docker](./robotics/docker.md) [ROS](./robotics/ros_logic.md)）
- **深度学习基础设施**：PyTorch / [TensorRT / ONNX Runtime](./robotics/edge_deployment.md)
- 👉 实战案例：[VLA 语音抓取 9终端全闭环](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md) · [行为树版 VLA](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) · [MCP 大模型 Tool Call](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md) · [模仿学习环境部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/8.imitation_learning.md)

#### 2.3.2 导航与建图 (Navigation & SLAM) 👉 [SLAM 专题](./robotics/slam.md) · [路径规划](./robotics/path_planning.md)
- ROS Navigation / Nav2（轮式全栈路径规划与避障）
- **SLAM**：2D/3D 激光（Cartographer/FAST-LIO）、V-SLAM（ORB-SLAM3）、回环检测、图优化
- **路径规划算法**：全局：A* / RRT* / PRM；局部：DWA / TEB / MPC 👉 详见 [路径规划专题](./robotics/path_planning.md)
- [FAST-LIO（LiDAR 里程计）](./robotics/slam.md)、[Docker 挂载](./robotics/docker.md) 踩坑
- 👉 实战案例：[地图导航与 FAST_LIO](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/3.map_navigation.md) · [官方导航集成](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/3.1official_navigation.md)

#### 2.3.3 机械臂与运动规划 (Manipulation) 👉 [经典动力学与运动控制](./robotics/dynamics_control.md)

- ROS MoveIt / MoveIt 2（运动规划、碰撞检测、[逆运动学](./robotics/dynamics_control.md)）
- IK 求解器：TRAC-IK（冗余自由度优化求解）
- OctoMap 3D 点云避障 + OMPL 路径规划
- **视觉抓取管线**：YOLO → TF2 坐标变换 → IK 逆解 → 轨迹生成 → 抓取执行
- **轨迹生成 (Trajectory Generation)**：最小 jerk / 最小 snap 平滑、B-spline / 五次多项式插值、时间参数化（Time-parameterization）、Via-points → 连续轨迹
- **抓取理论基础**：力封闭（Force Closure）/ 形封闭（Form Closure）、摩擦锥（Friction Cone）、抓取质量度量
- 👉 实战案例：[MoveIt 经典版/OctoMap 双轨抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/28.moveit_grasping.md) · [IK 逆运动学](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/9.IK.md) · [TF2 视觉抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.4real_visual_grasp.md) · [视觉抓取基础](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/6.visual_grasp.md)

#### 2.3.4 任务编排与逻辑调度

- **行为树 (Behavior Trees)**：py_trees，行为封装为独立节点，可组合/替换/插入，解决千行 if-else 状态机维护难题 👉 架构见 [ROS 架构逻辑](./robotics/ros_logic.md)
- 状态机 (State Machine)
- **AI Agent 工作流**：LangChain / CrewAI / n8n
- 👉 实战案例：[行为树版 VLA 抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md)

#### 2.3.5 LLM for Robotics（高层规划与工具调用） 👉 [LLM for Robotics 专题](./robotics/llm_for_robotics.md)

- **定位**：LLM 通常**不直接输出关节角**，而是做任务理解、分解、规划与 tool call（~1Hz System 2），低层交给 VLA / 行为树 / MoveIt
- **主要范式** 👉 [专题笔记](./robotics/llm_for_robotics.md)
 - **高层规划**：[PaLM-E](https://arxiv.org/abs/2303.03378) · [LLM+P](https://arxiv.org/abs/2304.11477)（LLM→PDDL→传统 planner）
 - **3D+LLM**：[VoxPoser](https://arxiv.org/abs/2307.05973) · [OmniManip](https://arxiv.org/abs/2501.03841)
 - **Code as Policy**：[CaP](https://arxiv.org/abs/2209.07753) · Instruction2Act（与 Kuavo V3 MCP 思路相近）
 - **评测**：[Embodied Agent Interface](https://embodied-agent-interface.github.io/)（测 LLM 任务理解/分解，不测低层执行）
- **与 Kuavo 对应**：V1 状态机 ≈ 符号规划 · V2 行为树 ≈ 分层编排 · V3 MCP ≈ Agent tool call
- 👉 实战案例：[MCP VLA 抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md) · [本地大模型语音](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/21.2.local_AI_large_model.md)

### 2.4 人机交互 (HRI)

- **显式交互**：语音指令、手柄/摇杆（H12 遥控器）、UI/Web 监控
- **隐式交互**：人脸识别与跟踪、手势识别、头部姿态跟随
- **全身表演动作**：太极、编舞、CSV 动作序列重放
- 👉 实战案例：[人脸识别](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/32.1.face_recognition.md) · [人脸跟踪融合](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/32.2.face_recognition_traking.md) · [头身协同视觉跟随](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/24.1.visual_tracking.md) · [H12 遥控器](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/17.h12_remote_control.md) · [太极全身动作](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/10.Tai_Ji.md) · [手臂编舞](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/13.arm_move.md) · [机器人舞蹈](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/14.robot_dance.md)

---

## 三、控制层（下位机 / “小脑” - Motion Control）

> 下位机负责"怎么动得稳"。在双足人形中，它是运行实时 OS 的高性能主机，负责 1kHz 动力学控制与安全兜底。
>
> **多速率控制架构**（人形实战）：[WBC/MPC](./robotics/dynamics_control.md) @ 1kHz（底层力矩）→ [RL](./robotics/RL.md) 策略推理 @ 50Hz（[ONNX](./robotics/edge_deployment.md)）→ 视觉感知 @ 30Hz → 大模型决策 @ 异步。各级之间通过低通滤波 + 线性插值平滑衔接，避免阶跃冲击。

### 3.1 控制硬件

#### 3.1.1 经典 MCU（轮式/普通机器人）
- ARM Cortex-M（STM32）、ESP32、Arduino

#### 3.1.2 高性能 PC 级（人形/多足机器人）
- x86 高性能主机（胸部 NUC），充当 ROS Master
- 工业 PLC / 多轴运动控制卡

### 3.2 操作系统与通信

#### 3.2.1 实时操作系统
- RT-Preempt（Linux 实时补丁，人形小脑必备）
- FreeRTOS / RT-Thread（MCU 级）
- VxWorks（商用高可靠）

#### 3.2.2 高速总线主站
- EtherCAT 主站（微秒级同步，全身几十个关节高频下发）
- CAN / CAN FD 主站

### 3.3 核心控制算法

#### 3.3.1 经典闭环控制 👉 [PID 控制专题](./robotics/pid_control.md)
- 独立关节 PID 控制律（P/I/D 三项 + 前馈）
- **级联控制**：电流环（20-100kHz）→ 速度环（1-5kHz）→ 位置环（100-1000Hz）
- **前馈控制**：[逆动力学前馈](./robotics/dynamics_control.md) + [PID](./robotics/pid_control.md) 反馈 = 零延迟 + 误差纠正
- 底盘运动学逆解（差速、全向轮）
- 里程计推算
- 抗积分饱和（Anti-windup）、低通滤波降噪

#### 3.3.2 高阶动力学与平衡控制 👉 [经典动力学与运动控制](./robotics/dynamics_control.md)
- **[全身控制 (WBC)](./robotics/dynamics_control.md)**：多任务层级优化，同时满足姿态/平衡/操作
- **逆运动学 (IK)**：雅可比矩阵 $J$，速度映射 $\dot{x}=J\dot{q}$，静力映射 $\tau=J^T F$
- **[模型预测控制 (MPC)](./robotics/dynamics_control.md)**：有限时域优化
- **ZMP** 动态平衡 / 质心规划 / 奇异点规避
- **阻抗/导纳控制** 👉 [阻抗控制专题](./robotics/impedance_control.md)：虚拟弹簧-阻尼-质量模型，刚度/阻尼参数调优，柔顺交互物理底座
- **双足平衡与抗扰动**：踝策略 → 髋策略 → 迈步策略（分级推恢复）、捕获点（Capture Point）理论
- **示教与重力补偿**：拖动示教 + 零力矩模式
- 👉 实战案例：[示教/重力补偿](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/18.teaching_gravity_compensation.md) · [上下楼梯仿真](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/5.up_down_stair.md)
- 👉 理论基础：[优化理论（QP/NLP在控制中的作用）](./robotics/optimization_theory.md)

#### 3.3.3 数据驱动运动控制 (Data-Driven Locomotion) 👉 [RL 笔记](./robotics/RL.md) · [世界模型详解](./robotics/world_model.md)

- **PPO 强化学习行走**：[Isaac Lab](./robotics/RL.md) 训练，87维 obs 跟踪 $(v_x, v_y, \omega)$，[ONNX 导出](./robotics/edge_deployment.md) → [MuJoCo Sim2Sim](./robotics/robot_modeling.md) → 真机部署
- **IL+RL 全身舞蹈**：CSV 动作参考轨迹 + mimic 跟踪奖励，115维 obs，4096 并行环境（8GB 显存）
- **TD-MPC2 世界模型**：隐式世界模型 + MPPI 规划，对比 model-based RL vs PPO 的样本效率
- **混合级联架构**（现代人形主流）：[RL](./robotics/RL.md) 充当高频直觉大脑 → [WBC/MPC](./robotics/dynamics_control.md) 在 1kHz 对 RL 输出做物理安全兜底
- **Sim2Real 核心痛点**：S49 机型 [URDF](./robotics/robot_modeling.md) 与训练资产版本撕裂，需手动缝合 `.info` 与 `humanoidController.cpp`；[ONNX](./robotics/edge_deployment.md) 观测空间对齐（CSV 关节顺序必须 100% 一致）
- 👉 实战案例：[RL 行走 Sim2Real 真机部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) · [奖励函数/域随机化拆解](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.2RL_lab_analysis_code.md) · [IL+RL 舞蹈总览](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.1.RL_dance_overview.md) · [S49 舞蹈训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.3.RL_dance_train.md) · [TD-MPC2 世界模型](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/31.1.world_model.md)

---

## 四、执行层（执行器 / “肌肉与神经末梢” - Actuators）

### 4.1 驱动级控制 👉 [FOC 矢量控制](./robotics/motor_foc.md)
- 关节级 MCU（内嵌伺服驱动板）
- **FOC 矢量控制**：Clarke/Park 变换、SVPWM、转矩/励磁解耦（$I_q$ 控力矩，$I_d$ 控磁场）
- 电流环 → 速度环 → 位置环（三环级联，内环频率 5-10× 外环）
- 功率变换电路（MOSFET/IGBT 逆变桥）

### 4.2 运动执行器
- 高扭矩无框力矩电机（人形关节主流）
- BLDC / PMSM / 伺服电机
- 直线电机 / 电动推杆 / 滚珠丝杠

### 4.3 传动与关节模组
- 谐波减速器（机械臂/双足高精轻量化）
- RV 减速器（高负载）· 行星减速器（机器狗关节）
- 一体化关节（减速器+电机+编码器+驱动板集成）
- 电磁抱闸（断电锁死保护）

### 4.4 末端执行器
- 灵巧手（多指独立驱动）/ 平行夹爪 / 柔性抓取器 / 真空吸盘
- 👉 实战案例：[夹爪安全与硬件调试](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/20.gripper_issue.md)

### 4.5 关节校准与维护
- 编码器零位偏移标定
- 关节刚度/阻尼参数辨识
- 官方升级覆盖魔改的 git stash / 手动合并流程
- 👉 实战案例：[关节标定](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/26.joint_calibration.md) · [官方包升级与排障](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/25.update.md)

---

## 五、机械结构层 (Mechanical Structure) 👉 [机器人建模（URDF/MJCF/USD）](./robotics/robot_modeling.md)

### 5.1 移动底盘形态 👉 [机器人分类与特性对比](./robotics/robot_types.md)
- 轮式（差速 / 全向 Mecanum / 阿克曼转向）
- 履带式 / 腿式（双足人形 / 四足机器狗）

### 5.2 骨架与外壳
- 航空铝合金切削 / 碳纤维框架（轻量化高刚度）
- 3D 打印 / 注塑 / 玻璃钢外壳

### 5.3 宏观传动机构
- 同步带 / 齿轮齿条 / 连杆机构 / 钢丝绳传动（灵巧手常用）

### 5.4 结构辅助件
- 精密轴承 / 联轴器 / 减震器

---

## 六、系统安全与防护机制 (Safety & Security)

> 贯穿软硬件的底层红线。本章大量内容来自真机实战，非书本理论。

### 6.1 真机物理安全 (Physical Safety SOP)

- **龙门架/安全绳配置**：触地后仅放 2-3cm 余量，触发触地判定 + 保留极限防坠
- **急停链路**：逻辑电/动力电分离架构——急停仅切断 48V 动力电，保留低压逻辑电以记录故障日志并维持网络
- **双人操作制度**：主操作员扶正躯干校准 IMU，安全员手悬急停
- **禁区划定**：机器人正前方与正后方 Pitch 轴方向严禁站人
- **低速空载先行**：首次点火前确认关节无异常啸叫

### 6.2 状态切换安全窗口

- 经典起立 → [RL](./robotics/RL.md) 接管：3 秒黄金窗口（[低刚度起立](./robotics/impedance_control.md) → 姿态稳定 → 按 B 键切换）
- 遥控器 E/F 档时序铁律（E 档最左 = 安全锁，F 档切换起立/站立）
- 起立前扶正躯干绝对垂直：校准内部 IMU 陀螺仪水平零点

### 6.3 软件与控制层安全

- 看门狗定时器（死机自动锁死）
- 异常状态机（故障分级响应与紧急停止）
- 碰撞检测与柔顺控制（遇异常阻力自动变软降刚度）
- 关节软限位（动态限制最大角度/速度/力矩）

### 6.4 网络与通信安全

- ROS 2 SROS / DDS 加密与访问控制
- 局域网隔离与高频控制网络防火墙策略

> 👉 真机安全 SOP 详见：[RL 行走 Sim2Real 安全部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md) · [舞蹈真机安全红线](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.1.RL_dance_overview.md)

---

## 七、通信系统 (Communication) 👉 [ROS 通信原理详解](./robotics/ros_communication.md)

### 7.1 内部总线与网络

#### 7.1.1 高速硬实时总线（小脑 ↔ 全身关节）
- EtherCAT（微秒级同步，链型拓扑）
- CAN / CAN FD（毫秒级同步）

#### 7.1.2 板级与外设
- UART / USB / SPI / I2C

#### 7.1.3 大脑与小脑通信（上位机 ↔ 下位机） 👉 [ROS 通信原理](./robotics/ros_communication.md) · [TF 树笔记](./robotics/tf_tree.md)

- **物理连接**：
 - 内部千兆以太网（机身骨架集成）
 - 静态 IP 局域网（下位机 `192.168.26.1`，上位机 `192.168.26.12`）
- **双机组网铁律**：
 - `ROS_MASTER_URI` 统一绑定下位机（`http://kuavo_master:11311`）
 - 各自暴露 `ROS_IP` 防止节点串台
 - 物理千兆网线直连，禁用 WiFi 传输控制指令
- **跨机用户权限隔离**：
 - 下位机运动节点：`root`（EtherCAT 总线需最高权限）
 - 下位机逻辑节点（TTS/行为树）：`lab` 普通用户（防 root 权限污染）
 - 上位机视觉/语音节点：`leju_kuavo` 用户
- **故障模式**：
 - 网络闪断 → ROS Topic 静默 → 机器人原地锁死（安全兜底）
 - 上位机死机 → 下位机独立运行 [WBC](./robotics/dynamics_control.md) 维持站立（不依赖上位机保活）
- **传输协议**：UDP（低延迟控制指令）· TCP（可靠配置传输）
- **核心数据流**：上位机下发视觉目标坐标 + 任务指令 → 下位机回传底盘状态 + 硬件报警
- 👉 实战案例：[上下位机网络配置](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/16.Internet.md)

### 7.2 外部遥测与交互
- Wi-Fi（局域网 SSH 调试）、Bluetooth（手柄接入）
- 4G/5G 蜂窝网络（云端大模型 API 接入）

---

## 八、电源系统 (Power System)

### 8.1 能源储备
- 高倍率动力锂电池组（满足瞬时爆发大电流）
- 超级电容（瞬时动态充放电补偿）

### 8.2 电池管理 (BMS)
- 电芯均衡 / 充放电保护
- SOC / SOH 状态估算与实时上报

### 8.3 电源转换与分配
- PDU 电源分配单元
- 多路 DC-DC 降压/升压模块（48V→12V/5V/3.3V）
- **急停开关 + 快熔断器**：逻辑电/动力电分离，拍下急停仅切断高压电机动力，保留低压逻辑控制电

---

## 九、开发、测试与工程化环境 (DevOps & Toolchain) 👉 [环境相关笔记](./robotics/environment.md)

> 👉 从零部署：[仿真/实机环境部署全流程](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/1.start.md) · [第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)

### 9.1 AI 原生开发环境
- Claude Code / Cursor：跨文件重构、架构咨询、代码生成
- VS Code + GitHub Copilot / JetBrains + Codex
- 👉 使用笔记：[Claude Code 配置](./ubuntu/claude_code_deepseek.md) · [Cursor 使用](./ubuntu/cursor.md) · [具身智能工程工具箱](./robotics/tools.md)

### 9.2 物理仿真与 Sim-to-Real 👉 [RL 笔记](./robotics/RL.md) · [环境笔记](./robotics/environment.md) · [模型部署](./robotics/edge_deployment.md) · [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)

- **[MuJoCo](./robotics/robot_modeling.md)**：轻量级动力学；[robosuite](https://robosuite.ai/) · LIBERO · Meta-World（操作 benchmark 生态）
- **Isaac Sim / Isaac Lab**：GPU 并行；[legged-gym](https://github.com/leggedrobotics/legged_gym) 腿足 RL（人形行走主线）
- **SAPIEN**：[ManiSkill](https://maniskill.readthedocs.io/) · [RoboTwin 2.0](https://github.com/robotwin-Platform/robotwin)（双臂操作 + 数据合成）
- **Gazebo**：经典 [ROS](./robotics/ros_logic.md) 移动机器人仿真
- **域随机化 (Domain Randomization)**：质量/摩擦/延迟随机噪声，Sim2Real 核心武器
- 👉 实战案例：[Isaac Lab 行走训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md) · [MuJoCo Sim2Sim](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.3RL_lab_sim_to_sim.md)

#### 9.2.1 评测基准与公开数据集 👉 [Benchmark 与 Dataset 专题](./robotics/benchmark_dataset.md)

> 仿真器决定「能造什么世界」；**Benchmark** 决定「怎么比」；**Dataset** 决定「学到什么分布」。建议跑通 **仿真器 + Benchmark + Dataset** 最小闭环。

- **操作 Benchmark**：[RoboTwin 2.0](https://github.com/robotwin-Platform/robotwin) · [LIBERO](https://libero-project.github.io/intro.html) · [CALVIN](http://calvin.cs.uni-freiburg.de/) · [Meta-World](https://meta-world.github.io/) · [SimplerENV](https://github.com/simpler-env/SimplerEnv)
- **规划 Benchmark**：[Embodied Agent Interface](https://embodied-agent-interface.github.io/)（LLM 决策链，不测低层执行）
- **跨本体 Dataset**：[Open X-Embodiment](https://robotics-transformer-x.github.io/) · [DROID](https://droid-dataset.github.io/) · [BridgeData V2](https://rail-berkeley.github.io/bridgedata/) · [白虎/青龙](https://www.openloong.org.cn/cn/dataset)
- **与 Kuavo 分工**：行走 RL → Isaac Lab 自定义 terrain；操作 VLA → 自采 LeRobot + 可选 RoboTwin/LIBERO 对照

### 9.3 调试、监控与可视化
- RViz（ROS 3D 空间呈现）· PlotJuggler · Foxglove Studio
- rqt_console（节点调试）· rosbag 录制与回放
- NVIDIA Nsight（CUDA 与渲染性能分析）
- 👉 实战案例：[抖动 rosbag 排障](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/19.tremble_rosbag.md)

### 9.4 容器化、版本控制与 C++ 工程 👉 [Docker 笔记](./robotics/docker.md) · [Git/GitHub 笔记](./robotics/git_github.md)

- **Docker**：容器化部署，Namespace 隔离 + Cgroups 限流，Volume 挂载
 - 👉 深度实战：[Docker 全生命周期 + 午夜排雷案例](./robotics/robotics_architecture_master_guide.md)
- **Git**：工作区/暂存区/本地仓库三层架构，子模块指针机制，`git stash -u` 保护魔改笔记
 - 👉 日常速查：[Git 拉取、子模块与系统清理](./robotics/git_pull.md)
- **C++ 工程化**（读/写机器人底层源码）
 - 👉 [Linux C++ 工业级项目方向](./robotics/linux_C++_project.md)
 - 👉 编程基础：[机器人底层 C++ 指南](./robotics/code/robotics_C++.md) · [C++ 语法补充](./robotics/code/C++_grammar_supplement.md) · [DSA 基础](./robotics/code/DSA_C++_Basics.md) · [DSA 树专题](./robotics/code/DSA_tree.md) · [机器人岗位技能对照](./robotics/code/Job_Requirements_for_Robot.md)
- **ROS 代码模板**：[ROS2 最小工作空间](./robotics/ros_code_template/ros2_code_ws/) · [ROS1 工作空间](./robotics/ros_code_template/ros1_code_ws/)
- CI/CD：GitHub Actions / GitLab CI（自动构建 + 仿真测试管道）
- 👉 开发工具链：[终端命令速查](./robotics/terminal_command.md) · [终端工具](./ubuntu/Terminal_tools.md) · [Conda 环境管理](./ubuntu/conda.md) · [代码阅读技巧](./robotics/code_read_skill.md) · [系统集成笔记](./robotics/robot_system_integration.md)

### 9.5 文档与项目管理
- Markdown 结构化文档 + Mermaid 架构图
- 👉 实战：[54 篇人形机器人二次开发文档](https://github.com/651yyds3939/kuavo-dev-notes) · [SDK 接口速查](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/%E6%8E%A5%E5%8F%A3%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3.md) · [资源链接汇总](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/999kuavo_resource.md)

---

> **备注**：这份思维导图不是一次写成的，而是在不断学习中完善的，也经历了很多次实机调试、炸机排障和架构重构后逐层沉淀下来的。每一层背后都有至少一篇实战笔记支撑。
>
> 通用知识库：[robotics-notes](https://github.com/651yyds3939/robotics-notes) · 项目实战：[kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)
