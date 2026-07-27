---
> **📌 文档定位：** 读源码 Survival Guide — 读 ROS 机器人 Python 应用层代码
> **适合：** 会基本 Python，要开始读/写二次开发脚本、感知节点、RL 训练脚本
> **前置：** [Python_C++_bridge](Python_C++_bridge.md)（分工地图）；Python 不熟 → [python_for_robotics_basics](python/python_for_robotics_basics.md)
> **后续：** RL 训练 → [RL.md](../RL.md)；部署端 C++ → [robotics_C++.md](robotics_C++.md)
> **预计时间：** 1 天
> **🏠 返回总索引：** [README.md](README.md)

# 🐍 机器人 Python 源码生存指南

**核心心法**：先跟数据流，再跟语法；Python 报错有行号，比 C++ Segfault 友好得多。
**适用场景**：阅读与开发基于 [ROS/ROS2](../ros_logic.md)、[AI/RL](../AI_learning_robotics.md) 的机器人**应用层** Python 代码。

> **链接规范**（与 [robot_system.md](../../robot_system.md) 一致）
>
> - **👉 专题笔记** → 本仓库 [`robotics/`](../)（相对路径）
> - **👉 实战案例** → [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（**GitHub 绝对链接**）

---

## 🗺️ 模块一：核心技能地图

读机器人 Python 代码，重点不是「Python 语法大全」，而是 **ROS 节点模式 + 消息流 + 常见库识谱**。

### 1. Python 四大战区（应用层）

| 核心战区 | 重点掌握内容 | 机器人实战场景 |
| --- | --- | --- |
| **ROS 节点与通信** | `rospy` / `rclpy`、Publisher/Subscriber、Service/Action | 发控制指令、收相机图像、调 IK 服务 |
| **消息与接口** | 自定义 msg/srv、`.msg` 字段、`cv_bridge` | 读官方 SDK 文档，填对话题名和字段 |
| **AI / 数据栈** | NumPy 切片、`torch.Tensor` 形状、OpenCV | 读 RL 训练脚本、处理图像和 obs |
| **工程编排** | launch、多进程、日志、`rospy.sleep` 时序 | 数据采集、VLA 多终端、训练点火 |

### 2. 和 C++ 读码的分工

| 你在 Python 代码里找什么 | 你在 C++ 代码里找什么 |
| --- | --- |
| 「谁发指令、谁调 AI、谁拼流程」 | 「谁跑控制环、谁算力矩、谁加载 ONNX」 |
| 业务逻辑、状态机、Prompt | 实时性、内存、CMake |

👉 对照：[Python_C++_bridge](Python_C++_bridge.md) · 读 C++ 见 [robotics_C++.md](robotics_C++.md)

---

## 🧠 模块二：认知跃迁 —— 脚本思维 vs 节点思维

| 维度 | 普通 Python 脚本 | ROS Python 节点 |
| --- | --- | --- |
| **运行方式** | `python3 script.py` 跑完即停 | 常驻进程，`spin()` 等消息 |
| **通信** | 函数调用、HTTP | Topic / Service / Action |
| **时序** | 顺序执行 | 回调驱动；常需 `sleep` 等物理动作 |
| **配置** | 命令行参数 | ROS Parameter / yaml |

> ⚠️ **高危实战坑点：发布太快**
> 创建 Publisher 后立刻 `publish()`，底层 C++ 订阅者可能尚未连上，**第一条指令会丢失**。务必先 `rospy.sleep(1.0)` 或 `rclpy` 等效等待。

👉 **实战案例**：[第一个 ROS 节点（四步法 + sleep 坑）](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)

---

## 📡 模块三：ROS Python 节点 —— 必读骨架

### 3.1 ROS 1：`rospy`（大量二次开发代码仍使用）

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

rospy.init_node('my_node')
pub = rospy.Publisher('/target_topic', String, queue_size=10)
rospy.sleep(1.0)          # 等订阅者就绪

msg = String()
msg.data = "hello"
pub.publish(msg)
rospy.spin()              # 若有订阅回调则阻塞在此
```

**读码时识别：**

| 代码 | 含义 |
| --- | --- |
| `rospy.init_node(...)` | 节点上户口 |
| `rospy.Publisher(...)` | 我要往某话题发数据 |
| `rospy.Subscriber(..., callback)` | 某话题来了就调 `callback` |
| `rospy.ServiceProxy(...)` | 调一个 C++ 提供的服务 |
| `rospy.sleep(t)` | 等 t 秒（等连接 / 等物理动作） |

### 3.2 ROS 2：`rclpy`（新模块优先）

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.pub = self.create_publisher(String, '/target_topic', 10)
        self.sub = self.create_subscription(
            String, '/input_topic', self.callback, 10)

    def callback(self, msg):
        self.get_logger().info(f'got: {msg.data}')
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

**读码时识别：**

| 代码 | 含义 |
| --- | --- |
| `class Xxx(Node)` | 节点是一个类 |
| `create_publisher` / `create_subscription` | 同 rospy，工厂方法 |
| `self.get_logger().info(...)` | 打日志 |
| `rclpy.spin(node)` | 事件循环 |
| `create_timer` | 定时回调（类似 ROS 定时器） |

👉 入门模板：[ROS2 Python 最小节点](../ros_code_template/ros2_code_ws/src/py_pkg/py_pkg/template.py) · 专题：[ROS2 开发流程](../ros2_process.md)

### 3.3 参数（Parameter）

**ROS 2 示例：**

```python
self.declare_parameter('max_speed', 0.5)
speed = self.get_parameter('max_speed').value
```

**读码要点：** 参数多在 launch 或 yaml 里注入；改行为先查 launch，不一定改源码。

👉 示例：[ROS2 参数模板](../ros_code_template/ros2_code_ws/src/py_pkg/py_pkg/parameter.py)

### 3.4 Launch 编排

- **ROS 1**：XML launch 或 Python launch
- **ROS 2**：**Python Launch** 为主（`launch_ros`），可编程分支（仿真/实机）

Launch **不写业务**，只负责：起哪些节点、传哪些参数、命名空间隔离。

👉 专题：[ROS 架构逻辑 § Launch](../ros_logic.md)

---

## ⚡ 模块四：Python 节点 vs C++ 节点 —— 何时用哪个

| 场景 | 推荐 | 原因 |
| --- | --- | --- |
| 视觉检测、LLM、语音 | **Python** | AI 库原生支持 |
| 发关节/底盘指令（低频） | **Python** | SDK 示例多为 Python |
| 数据采集、rosbag 分析 | **Python** | 迭代快 |
| 任务编排、行为树原型 | **Python** (`py_trees`) | 改逻辑不需编译 |
| RL 训练脚本 | **Python** | PyTorch 生态 |
| 1 kHz 控制环 | **C++** | Python 不可 |
| 嵌入控制器的 ONNX 推理 | **C++** | 见 [边缘部署](../edge_deployment.md) |
| 长期真机常驻、怕 GC 卡顿 | **C++** | 顶层调度可考虑 C++ 行为树 |

**二次开发默认选 Python**；只有性能/实时/部署进控制环时再考虑 C++。

---

## 🧩 模块五：常见应用层场景识谱

读源码时，见到文件名/目录可快速归类：

| 场景 | 典型文件特征 | 读码关注点 |
| --- | --- | --- |
| **数据采集** | `record` · `lerobot` · `episode` · `rosbag` | 订阅哪些 obs/action topic，存什么格式 |
| **Joystick / 遥控** | `joystick` · `teleop` · `keyboard` | 按键映射到哪条 Topic/Service |
| **RL 训练** | `train.py` · `rsl_rl` · `env.yaml` · `reward` | obs 维度、奖励项、域随机化 |
| **顶层调度** | `py_trees` · `state_machine` · `master` · `demo.py` | 状态转移条件、调了哪些 Service |
| **感知节点** | `yolo` · `detect` · `cv_bridge` · `tf2` | 输入图像 topic，输出检测/坐标 topic |
| **大模型网关** | `flask` · `asr` · `tts` · `llm` | HTTP/ROS 边界，Prompt 解析逻辑 |

👉 **实战案例**：[LeRobot 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) · [舞蹈训练终端命令](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.7.RL_dance_terminal_commands.md) · [行为树版 VLA](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) · [Isaac Lab 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md)

---

## 🔢 模块六：NumPy / PyTorch 识谱（读 RL 代码够用）

不展开深度学习课程，只建立**读码反射**。

### 6.1 NumPy

```python
obs = np.array([1.0, 2.0, 3.0])   # 一维向量
obs.shape                          # (3,) — 读 RL 代码先看 shape
obs[0:3]                           # 切片
np.concatenate([a, b])             # 拼接 obs
```

**RL 常见：** obs 是长度 N 的向量；读 `env.yaml` 或 `cfg` 里的 `num_observations`。

### 6.2 PyTorch（训练脚本）

```python
x = torch.randn(1, 87)            # batch=1, obs_dim=87
model.eval()                       # 推理模式
with torch.no_grad():             # 不建计算图
    action = policy(x)
torch.onnx.export(...)             # 导出给 C++ 部署
```

**读码顺序：** `train.py` → 环境 obs 构造 → `ActorCritic` 输入输出维度 → 奖励函数。

👉 专题：[RL.md](../RL.md) · [边缘部署](../edge_deployment.md)
👉 **实战案例**：[RL 奖励/域随机化拆解](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.2RL_lab_analysis_code.md) · [Sim2Real 部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md)

---

## 🔍 模块七：实战拆解 —— 解剖一段 Python 节点

```python
from my_robot_msgs.srv import IkService
proxy = rospy.ServiceProxy('/ik/solve', IkService)
resp = proxy(request)
```

**逻辑直译：**

1. *`my_robot_msgs.srv.xxx`*：：自定义**服务**类型（请求/响应结构体）。
2. **`ServiceProxy`**：我不实现服务，只**调用**别人（通常是 C++ 节点）提供的服务。
3. **`resp = proxy(request)`**：同步等待 C++ 算完 IK 返回结果。

**规律：** Python 二次开发大量代码是 **「ServiceProxy + Publisher」**，真正算题的在 C++。

👉 **实战案例**：[SDK 接口速查](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/接口使用文档.md) · [IK 逆运动学](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/9.IK.md)

---

## ☠️ 模块八：崩溃自救 —— Traceback 排雷指南

Python 崩溃会给出**完整堆栈**，比 C++ Segfault 友好。

### 8.1 常见报错与对策

| 报错 | 含义 | 自救 |
| --- | --- | --- |
| `ImportError: No module named xxx` | 缺包或没 source 工作空间 | `pip install` / `source devel/setup.bash` |
| `rospy.ROSException: timeout` | 服务/话题不存在或没启动 | `rostopic list` 检查节点是否起来 |
| `KeyError` / `AttributeError` | 消息字段名写错 | 对照 `.msg` / 接口文档 |
| `CvBridge Error` | 图像编码不对 | 检查 `encoding` 参数 |
| `CUDA out of memory` | 训练 batch/环境数太大 | 减 `num_envs` 或 batch size |
| `IndentationError` | 缩进错误 | Python 经典 |

### 8.2 Python vs C++ 调试对比

| | Python | C++ |
| --- | --- | --- |
| 报错信息 | Traceback + 行号 | 常只有 `Segfault` |
| 改完生效 | 直接重跑 | 常需重新编译 |
| 常用工具 | `print` / `pdb` / `ipdb` | `gdb` / `Valgrind` |
| 日志 | `rospy.loginfo` / `get_logger()` | `RCLCPP_INFO` / `ROS_INFO` |

### 8.3 读 Python 机器人代码的推荐顺序

```text
1. 看 launch 文件 → 起了哪些节点
2. 看节点 main / __init__ → 订阅/发布了什么
3. 跟 callback / 主循环 → 数据处理逻辑
4. 看到 ServiceProxy → 跳到接口文档查 C++ 侧
5. 看到 torch/numpy → 先 print .shape
```

---

## 💡 模块九：Ultimate 口诀 —— 机器人 Python 读码检查清单

打开任意 `.py` 机器人节点，按顺序过一遍：

1. **ROS 版本？** `import rospy` → ROS 1；`import rclpy` → ROS 2
2. **输入从哪来？** Subscriber / Service 响应 / 参数
3. **输出到哪去？** Publisher / Service 请求 / 文件/网络
4. **有没有 sleep？** 等连接？等物理动作？
5. **有没有调 C++？** ServiceProxy → 核心算力在底层
6. **时序对不对？** 先站立再动手臂？先检测再 IK？

---

## 📍 文档导航

| 方向 | 文档 |
| --- | --- |
| 🏠 总索引 | [README.md](README.md) |
| Python/C++ 分工 | [Python_C++_bridge.md](Python_C++_bridge.md) |
| Python 最小语法 | [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md) |
| 读 C++ 源码 | [robotics_C++.md](robotics_C++.md) |
| ROS 专题 | [ros_logic.md](../ros_logic.md) · [ros_communication.md](../ros_communication.md) |
| RL / 部署 | [RL.md](../RL.md) · [edge_deployment.md](../edge_deployment.md) |
| ROS2 代码模板 | [ros2_code_ws/py_pkg](../ros_code_template/ros2_code_ws/src/py_pkg/) |
| 👉 实战索引 | [kuavo-dev-notes/kuavo_notes](https://github.com/651yyds3939/kuavo-dev-notes/tree/master/kuavo_notes) |
