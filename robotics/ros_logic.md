# ROS 架构逻辑：从「一堆节点」到「可维护的系统」

> **核心定位**：[`ros_communication.md`](./ros_communication.md) 讲**节点之间怎么说话**（Topic/Service/Action/参数）；[`ros2_process.md`](./ros2_process.md) 讲**怎么建包、编译、跑起来**。本篇讲中间层——**为什么这样拆节点、包和工作空间**，以及 ROS 1 / ROS 2 在架构上的根本差异。
>
> 👉 入门代码模板：[ROS2 最小工作空间](./ros_code_template/ros2_code_ws/) · [ROS1 工作空间](./ros_code_template/ros1_code_ws/)

---

## 一、三层物理结构：Workspace → Package → Node

| 层级 | 是什么 | 类比 |
|------|--------|------|
| **Workspace（工作空间）** | 放多个功能包的目录树，`src/` + `build/` + `install/` | 整个「机器人软件项目」 |
| **Package（功能包）** | 可独立编译、发布的最小单元，含节点、消息、launch、配置 | 一个「子系统模块」（导航、感知、控制） |
| **Node（节点）** | 真正跑起来的进程，一个 `.cpp` / `.py` 的 `main()` | 一个「专职工人」 |

**架构铁律**：一个节点只做一件事。感知节点只发布传感器数据，规划节点只算路径，控制节点只下发力矩——**禁止**在一个节点里又读相机又算 IK 又发电机指令（否则无法单独重启、无法分布式部署、无法单元测试）。

---

## 二、ROS 1 vs ROS 2：架构范式的分水岭

| 维度 | ROS 1 | ROS 2 |
|------|-------|-------|
| **拓扑** | 中心化：`roscore`（Master）登记所有节点 | 去中心化：DDS 自动发现，无 Master |
| **多机** | 必须配置 `ROS_MASTER_URI` + `ROS_IP`，易串台 | 同一 DDS Domain 内即互通，但仍需网络隔离策略 |
| **实时性** | 无硬实时保证 | 可选 `rclcpp::Node` + 实时内核 / 执行器优先级 |
| **生命周期** | 节点启动即运行 | 支持 `LifecycleNode`（未配置 → 非激活 → 激活 → 关闭） |
| **硬件抽象** | 各厂商各自封装 | `ros2_control` 统一 Hardware Interface |

**人形机器人实战**：双足人形等双机架构仍常见 **ROS 1 Noetic 在下位机**（历史包袱 + 驱动生态），上位机视觉/语音可 ROS 1 或独立进程；新模块优先 ROS 2 时需规划 **ROS 1 ↔ ROS 2 桥接**（`ros1_bridge`）。

---

## 三、计算图 (Computation Graph) 设计

ROS 系统的运行时形态是一张**有向图**：

- **节点** = 顶点
- **Topic 数据流** = 边（异步、连续）
- **Service / Action** = 请求-响应或长任务的「临时边」
- **TF 树** = 并行的坐标系变换图（见 [`tf_tree.md`](./tf_tree.md)）

### 3.1 典型分层（与思维导图对应）

```text
感知层节点  →  /camera/image, /scan, /imu
      ↓
决策层节点  →  /goal, /detected_objects, /task_command
      ↓
规划层节点  →  /planned_path, /joint_trajectory
      ↓
控制层节点  →  /joint_commands, /wrench
      ↓
驱动/硬件接口  →  EtherCAT / CAN 主站
```

**数据流原则**：

1. **高频数据走 Topic**，低频配置走 Parameter / Service。
2. **控制环内禁止阻塞调用**（不要在 1kHz 回调里 `call()` 一个慢 Service）。
3. **消息类型即接口契约**——改 `.msg` 字段等于改 API，需版本管理与向后兼容。

### 3.2 Launch 文件：系统的「接线图」

Launch 不负责业务逻辑，只负责**一次性把计算图搭好**：

- 启动哪些节点、传哪些参数
- 命名空间 (`ns`) 隔离多机器人
- 条件启动（仿真 vs 实机）

ROS 2 使用 Python Launch（`launch_ros`），可编程分支，比 ROS 1 XML launch 更灵活。

---

## 四、参数系统与配置管理

| 机制 | 用途 |
|------|------|
| **Parameter** | 节点运行时配置（[PID 增益](./pid_control.md)、话题名 remap、开关） |
| **YAML 配置** | 启动时批量注入参数（launch 加载）；版本化配置建议纳入 [Git](./git_github.md) 管理 |
| **Remapping** | 不改代码，把 `/cmd_vel` 映射到 `/robot/cmd_vel` |

**最佳实践**：可热调参数放 Parameter Server；版本化配置放 Git 管理的 YAML；**不要把密钥写进 launch 文件**。

---

## 五、ros2_control：硬件在架构中的位置

`ros2_control` 把「真机 / 仿真 / 回放」抽象成统一的 **Hardware Interface**：

- **Controller Manager** 按频率调度控制器（位置、速度、力矩）
- **Resource Manager** 管理关节句柄
- 仿真与实机切换 = 换 Hardware Plugin，**上层规划节点无感**

这是思维导图 2.2.2 中「统一管理真实硬件与仿真切换」的架构落点。

---

## 六、常见反模式（架构腐化信号）

| 反模式 | 后果 | 正确做法 |
|--------|------|----------|
| 「上帝节点」包揽感知+规划+控制 | 无法调试、无法多机、一处崩溃全挂 | 按职责拆节点 |
| 用 Service 传 30Hz 图像 | 阻塞、延迟爆炸 | 改用 Topic |
| 不看 TF 树直接硬编码坐标 | 标定/换传感器后全线失效 | 统一走 TF2 |
| 多机共用一个 `ROS_MASTER_URI` 但未设 `ROS_IP` | 节点注册到错误机器 | 双机组网铁律（见思维导图第七章） |
| 魔改官方包却不 fork / 不 submodule | 官方升级覆盖本地修改 | 见 [`git_github.md`](./git_github.md) · [`robotics_architecture_master_guide.md`](./robotics_architecture_master_guide.md) |

---

## 七、与专题笔记的导航关系

| 若需… | 去看 |
|--------|------|
| 搞清 Topic/Service/Action 怎么选 | [`ros_communication.md`](./ros_communication.md) |
| 创建第一个 ROS2 包并编译 | [`ros2_process.md`](./ros2_process.md) · [`ros_code_template/`](./ros_code_template/) · [工作空间文件速查](./doc_concept.md) |
| 理解 map/odom/base_link | [`tf_tree.md`](./tf_tree.md) |
| 混合工作空间 / 编译污染 | [`environment.md`](./environment.md) |
| Docker 里跑整套 ROS | [`docker.md`](./docker.md) |
| 系统集成数据流总览 | [`robot_system_integration.md`](./robot_system_integration.md) |
