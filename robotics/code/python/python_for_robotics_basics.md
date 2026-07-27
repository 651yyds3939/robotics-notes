---
> **📌 文档定位：** 刷题刀 — 机器人 Python 最小必要语法（非语法大全）
> **适合：** 完全不会 Python、准备读 ROS 节点或 RL 训练脚本
> **前置：** 无
> **后续：** [robotics_Python.md](../robotics_Python.md) → ROS 节点读码
> **相关：** 已有 Python/RL 经验可跳过本文，直接 👉 [第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md) · [RL 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md)
> **预计时间：** 1–2 天
> **🏠 返回总索引：** [README.md](../README.md)

# Python 机器人开发最小必要语法清单

面向 ROS 二次开发与 RL 脚本的**最小语法**（跳过 Web 开发、数据分析高阶特性）。

掌握以下五个板块后，即可开始读 [robotics_Python.md](../robotics_Python.md) 里的 ROS 节点代码。

---

## 一、基础类型与控制流

### 1.1 基本数据类型

| 类型 | 示例 | 机器人场景 |
| --- | --- | --- |
| `int` | `motor_id = 1` | 关节编号 |
| `float` | `angle = 30.0` | 角度、速度 |
| `bool` | `is_grasped = True` | 状态标志 |
| `str` | `target = "bottle"` | LLM 输出类别 |
| `None` | `result = None` | 未初始化 |

### 1.2 控制流

```python
if speed > 0.5:
    print("too fast")
elif speed > 0.1:
    print("ok")
else:
    print("stop")

for i in range(10):
    print(i)

for joint in joint_list:
    print(joint)

while not done:
    step += 1
```

---

## 二、容器：列表与字典（最高频）

机器人 Python 代码里，**list 和 dict 比任何其他结构都常见**。

### 2.1 列表 `list`

```python
joints = [0.0, 30.0, -15.0]      # 关节角数组
joints.append(10.0)               # 追加
len(joints)                       # 长度
joints[0]                         # 下标访问
joints[1:3]                       # 切片
```

### 2.2 字典 `dict`

```python
cmd = {"action": "grab", "target": "apple"}
cmd["target"]                     # 取值
cmd.get("target", "default")      # 安全取值
"action" in cmd                   # 键是否存在
```

**RL / VLA 常见：** LLM 输出 JSON → Python `dict` → 查键决定下一步动作。

---

## 三、函数与模块

### 3.1 函数

```python
def clamp_angle(angle, lo=-30, hi=30):
    if angle < lo:
        return lo
    if angle > hi:
        return hi
    return angle
```

### 3.2 导入（读代码时天天见）

```python
import rospy                          # 导入整个模块
from std_msgs.msg import String       # 从模块导入类
from my_pkg.msg import JointCmd       # 自定义消息
```

**读码规则：** 看 `from xxx import yyy` 就知道节点依赖哪些 ROS 包。

### 3.3 `if __name__ == '__main__'`

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

表示：**被 import 时不自动执行，直接运行时执行 main**。

---

## 四、类与对象（读 ROS 2 节点必备）

ROS 2 节点几乎都是「继承 `Node` 的类」。

```python
class ArmController:
    def __init__(self, name):
        self.name = name
        self.speed = 0.0

    def move(self, target):
        self.speed = target

ctrl = ArmController("left_arm")
ctrl.move(0.5)
```

| 概念 | 含义 |
| --- | --- |
| `class` | 定义一种「模板」 |
| `__init__` | 构造函数，创建对象时自动调用 |
| `self` | 对象自身（类似 C++ 的 `this`） |
| `self.xxx` | 成员变量 |

---

## 五、文件操作与虚拟环境

### 5.1 读写文件（配置、CSV、日志）

```python
with open("config.yaml", "r") as f:
    text = f.read()

with open("log.txt", "a") as f:
    f.write("episode done\n")
```

### 5.2 虚拟环境（RL 训练必会）

```bash
# 创建
python3 -m venv ~/my_env
# 或 Conda
conda create -n isaaclab python=3.10

# 激活
source ~/my_env/bin/activate
conda activate isaaclab

# 安装依赖
pip install torch numpy
```

**机器人常见：** 训练环境（Isaac Lab）与 ROS 环境**分开**，避免包冲突。

---

## 六、读 RL 脚本时的最小 NumPy 补充

```python
import numpy as np

obs = np.zeros(87)                # 87 维观测
obs.shape                         # (87,)
np.array([1, 2, 3])               # 从 list 转数组
obs + 1                           # 逐元素运算
```

够用来**读** `env.get_obs()` 和配置文件里的维度，不必深入线性代数。

---

## 🛠️ 避坑指南：哪些 Python 语法现在「先不要深啃」

| 先跳过 | 原因 |
| --- | --- |
| 装饰器、元类 | 读 ROS 节点初期几乎不遇 |
| 异步 `async/await` | 少数网关代码才用 |
| 多进程/多线程深入 | 先会 `rospy.spin` 即可 |
| 类型标注 `typing` | 有更好，没有也能读 |
| 大型 Web 框架 | 机器人里 Flask 够用 |

---

## 🏁 建议起步

1. 对照上文清单自检，能盲写含 `list`/`dict`/函数/`class` 的小脚本
2. 读 👉 [第一个 ROS 节点](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)
3. 进入 [robotics_Python.md](../robotics_Python.md) 学 ROS 节点读码

**已有 Python + RL 经验：** 跳过本文，直接从 [robotics_Python.md](../robotics_Python.md) 或 👉 [15.1 RL 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md) 开始。

---

## 📍 文档导航

| 方向 | 文档 |
| --- | --- |
| 🏠 总索引 | [README.md](../README.md) |
| Python/C++ 分工 | [Python_C++_bridge.md](../Python_C++_bridge.md) |
| **Python 最小语法（本文）** | [python_for_robotics_basics.md](python_for_robotics_basics.md) |
| 读 Python 机器人源码 | [robotics_Python.md](../robotics_Python.md) |
| 读 C++ 源码 | [robotics_C++.md](../robotics_C++.md) |
| 👉 第一个 ROS 节点 | [2.first_node](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md) |
