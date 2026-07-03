# Benchmark 与 Dataset —— 具身智能评测与数据生态

> **核心定位**：仿真器决定「能造什么世界」；**Benchmark** 决定「用什么任务、什么协议比好坏」；**Dataset** 决定「模型学到什么行为分布」。研究复现常需跑通 **一个仿真器 + 一个 Benchmark + 一个 Dataset** 最小闭环。
>
> 👉 思维导图位置：[9.2.1 评测基准与公开数据集](../robot_system.md) · [1.6 数据采集](../robot_system.md)
>
> 外部索引：[Embodied-AI-Guide · infrastructure.md](https://github.com/TianxingChen/Embodied-AI-Guide/blob/main/topics/infrastructure.md) · [Simulators Wiki](https://simulately.wiki/)

---

## 一、三者关系

```
Simulator（仿真器）  →  物理世界
Benchmark           →  任务集 + 评测协议 + 指标
Dataset             →  训练用轨迹（obs, action, language…）
```

读 Dataset 时关注四件事：**(1) 真实 vs 仿真 (2) 同构 vs 异构 (3) 模态 (4) 是否附带采集/训练代码**。

---

## 二、仿真器 × Benchmark 映射

| 仿真器 | 典型 Benchmark / 工具链 | 链接 |
|--------|-------------------------|------|
| **IsaacGym / Isaac Lab** | legged-gym、parkour（腿足 RL） | [legged_gym](https://github.com/leggedrobotics/legged_gym) |
| **MuJoCo** | robosuite、LIBERO、Meta-World、RoboCasa | [LIBERO](https://libero-project.github.io/main.html) |
| **SAPIEN** | ManiSkill、RoboTwin 2.0（双臂操作） | [RoboTwin](https://github.com/robotwin-Platform/robotwin) |
| **CoppeliaSim** | RLBench、PerAct2 | [RLBench](https://github.com/stepjam/RLBench) |
| **PyBullet** | CALVIN、Ravens | [CALVIN](https://github.com/mees/calvin) |
| **Gazebo** | ROS 移动机器人、Nav2 | [gazebosim.org](https://gazebosim.org) |

**与 Kuavo 工作对应**：

| 方向 | 常用组合 |
|------|----------|
| 人形行走 RL（`leju_robot_rl`） | Isaac Lab + 自定义 terrain（locomotion 线） |
| 操作 / VLA | RoboTwin、LIBERO、CALVIN（manipulation 线） |
| 自采数据 | LeRobot 格式（见 Kuavo 实战） |

---

## 三、主要 Benchmark（按研究问题）

### 3.1 操作 / Manipulation

| Benchmark | 一句话 | 链接 |
|-----------|--------|------|
| **RoboTwin 2.0** | 双臂；程序化合成 + 50 评测任务 | [GitHub](https://github.com/robotwin-Platform/robotwin) |
| **LIBERO** | 终身学习；顺序学任务后泛化 | [官网](https://libero-project.github.io/intro.html) |
| **CALVIN** | 语言条件 + 长视野多步操作 | [官网](http://calvin.cs.uni-freiburg.de/) |
| **Meta-World** | 50 操作任务；多任务 / 元 RL | [官网](https://meta-world.github.io/) |
| **SimplerENV** | 轻量快速对比操作策略 | [GitHub](https://github.com/simpler-env/SimplerEnv) |
| **RLBench** | 经典 tabletop 操作 | [GitHub](https://github.com/stepjam/RLBench) |

### 3.2 规划 / 决策（不测低层执行）

| Benchmark | 一句话 | 链接 |
|-----------|--------|------|
| **Embodied Agent Interface** | 测 LLM 任务理解/分解/序列化 | [官网](https://embodied-agent-interface.github.io/) |
| **RoboGen** | 程序化生成任务/场景/标注 | [GitHub](https://github.com/Genesis-Embodied-AI/RoboGen) |

---

## 四、主要 Dataset

### 4.1 大规模跨本体（训通用策略）

| 数据集 | 特点 | 链接 |
|--------|------|------|
| **Open X-Embodiment (RT-X)** | 22 种机器人、百万级轨迹 | [官网](https://robotics-transformer-x.github.io/) |
| **DROID** | 7.6 万轨迹；附硬件与训练代码 | [官网](https://droid-dataset.github.io/) |
| **BridgeData V2** | 6 万轨迹；语言 + 目标图像 | [Berkeley](https://rail-berkeley.github.io/bridgedata/) |
| **AgiBot World** | 百万级；同构；工业化采集 | [agibot-world.com](https://agibot-world.com/) |
| **ARIO** | 五模态；操作 + 导航 | [项目页](https://imaei.github.io/project_pages/ario/) |
| **白虎（青龙）** | 异构机器人；跨平台 | [openloong.org.cn](https://www.openloong.org.cn/cn/dataset) |

### 4.2 数据生成 / 扩增

| 框架 | 思路 | 链接 |
|------|------|------|
| **MimicGen** | 少量 demo → robosuite 仿真扩增 | [GitHub](https://github.com/NVlabs/mimicgen) |
| **DexMimicGen** | 双臂桌面；real2sim2real | [GitHub](https://github.com/NVlabs/dexmimicgen/) |
| **RoboTwin 2.0** | 程序化合成双臂数据 | [GitHub](https://github.com/robotwin-Platform/robotwin) |

### 4.3 采集范式（与 1.6 遥操作对应）

| 范式 | 代表 | 特点 |
|------|------|------|
| **主从双臂遥操作** | ALOHA | 高精度 action + 多视角 |
| **可穿戴 retargeting** | UMI | 人体示教 + 动作映射 |
| **第一人称视频** | Ego-centric | 低成本；弱 action 标注 |
| **自采（Kuavo）** | LeRobot v3.0 | 三机分工；见 kuavo-dev-notes |

---

## 五、选型建议

| 目标 | 优先看 |
|------|--------|
| 复现 OpenVLA / Octo | Open X-Embodiment + SimplerENV |
| 双臂操作入门 | RoboTwin 2.0 + ACT |
| 人形行走论文对比 | Isaac Lab + 自定义协议（尚无统一 benchmark） |
| Kuavo 自研 VLA | 自采 LeRobot + 自建评测任务 |

---

## 六、相关专题

- [RL 与仿真平台](./RL.md)
- [VLA 研究版图](./vla_landscape.md)
- [机器人建模 / MuJoCo · URDF](./robot_modeling.md)
- [环境部署](./environment.md)

---

> 👉 **Kuavo 实战**：[LeRobot 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) · [Isaac Lab 训练](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md)
