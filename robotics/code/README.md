# 🤖 机器人 C++ / Python 与算法学习笔记 — 总索引

> 本目录是一套**场景化、可执行**的学习材料，面向机器人二次开发、RL 与求职。
> **不确定该学 Python 还是 C++？** 先看 [Python_C++_bridge.md](Python_C++_bridge.md)。
> **从这里开始**，再按需跳转到各专题文档。

---

## 📚 文档一览

| 文档 | 角色 | 适合谁 | 预计时间 |
| --- | --- | --- | --- |
| [Python_C++_bridge.md](Python_C++_bridge.md) | **通用分工地图**：二次开发中 Python vs C++ | 不清楚该写 `.py` 还是碰 `.cpp` | 30 min |
| [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md) | **Python 刷题刀**：最小必要语法 | Python 零基础 | 1–2 天 |
| [robotics_Python.md](robotics_Python.md) | **读 Python 源码 Survival Guide** | 读 ROS 应用层 / RL 训练脚本 | 1 天 |
| [DSA_C++_Basics.md](DSA_C++_Basics.md) | **C++ 刷题刀**：LeetCode 最小语法 | 准备刷 Hot 100 | 1–2 天 |
| [C++_grammar_supplement.md](C++_grammar_supplement.md) | **写 C++ 手册**：OOP、智能指针、STL | 要写 C++ 类/行为树 | 2–3 天 |
| [robotics_C++.md](robotics_C++.md) | **读 C++ 源码 Survival Guide** | 读 ROS/MPC 底层代码 | 1 天 |
| [Job_Requirements_for_Robot.md](Job_Requirements_for_Robot.md) | **地图**：岗位 + 行为树项目路线 | 定方向 | 30 min |
| [data_stuctures_and_algorithms.md](data_stuctures_and_algorithms.md) | **方法论**：四步破局法 | 刷题卡语法 | 20 min |
| [DSA_tree.md](DSA_tree.md) | **树专题清单** | 刷树 Hot 100 | 1–2 周 |

---

## 🧭 我现在该看哪篇？（决策树）

```text
              不确定 Python 还是 C++？ → Python_C++_bridge.md
                              │
                    你想做什么？
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    定职业方向      刷 LeetCode      机器人二次开发/读源码
         │               │               │
         ▼               ▼               ▼
  Job_Requirements   DSA_C++_Basics   Python 不熟？
                           │               │
                           ▼          是 → python_for_robotics_basics
                  data_stuctures...          │
                  (四步破局法)               ▼
                           │          robotics_Python.md
                      DSA_tree         (ROS 节点/RL 脚本)
                      (树刷题)              │
                           │          要读 C++ 底层 ↓
                           │          DSA_C++_Basics → robotics_C++.md
```

**快速判断：**

- 不清楚 Python/C++ 分工 → [Python_C++_bridge.md](Python_C++_bridge.md)
- Python 零基础 → [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md)
- 读 ROS Python 节点 / RL 脚本 → [robotics_Python.md](robotics_Python.md)
- 完全零基础 C++（刷题） → [DSA_C++_Basics.md](DSA_C++_Basics.md)
- 读 C++ 控制源码 → [robotics_C++.md](robotics_C++.md)
- 定方向 / 行为树项目 → [Job_Requirements_for_Robot.md](Job_Requirements_for_Robot.md)

---

## 🛤️ 推荐学习路径

### 路径 A：刷 LeetCode 入门（1–2 周）

```text
DSA_C++_Basics
    → data_stuctures_and_algorithms（四步破局法）
    → DSA_tree（15 道树题）
    ↘ 语法盲点 ↗ C++_grammar_supplement
```

**通关标准：** 链表反转、二叉树遍历、两数之和。

---

### 路径 B：读 ROS C++ 底层源码

```text
Python_C++_bridge → DSA_C++_Basics → robotics_C++.md
    ↘ 类/多态/智能指针 ↗ C++_grammar_supplement
```

**通关标准：** 从 `.h` 看出订阅/发布，在 `.cpp` 跟完主逻辑。

---

### 路径 C：C++ 行为树项目（进阶）

```text
Python_C++_bridge → Job_Requirements
    → C++_grammar_supplement → DSA_tree（144/104）
    → robotics_C++.md → 行为树 MVP + 真机部署
```

---

### 路径 D：二次开发 / Python 主线（推荐大多数同学）

```text
Python_C++_bridge（弄清应用层与底层分工）
    → python_for_robotics_basics（Python 零基础才看）
    → robotics_Python.md（ROS 节点读码主文档）
    ↘ 实战案例 ↗
        · ROS Python 入门：[2.first_node](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/2.first_node.md)
        · RL 训练：[15.1](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.1.RL_lab_train.md) · [23.1 舞蹈概览](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/23.1.RL_dance_overview.md)
        · RL 理论：[RL.md](../RL.md)
        · 部署：[edge_deployment.md](../edge_deployment.md) · [15.4 Sim2Real](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md)
    → 需要读 C++ 部署端时 ↗ robotics_C++.md
```

**通关标准：** 能独立写 Python ROS 节点调官方接口；能打开 RL 训练脚本说出 obs 维度和奖励结构；说清哪些能力在 C++ 底座里。

---

## 🔗 文档间关系图

```text
                         README.md
                              │
              ┌───────────────┼───────────────┐
              │               │               │
       Python_C++_bridge   Python 线         C++ 线
              │               │               │
              │    python_for_robotics_basics │
              │               │               │
              │        robotics_Python        DSA_C++_Basics
              │               │               │
              │          (kuavo-dev-notes     grammar_supplement
              │           实战 GitHub)             │
              │               │           robotics_C++.md
              └───────────────┴───────────────┘
                          汇到实战项目
```

---

## 📋 知识点主文档索引

| 知识点 | 主文档 |
| --- | --- |
| Python vs C++ 分工 | [Python_C++_bridge](Python_C++_bridge.md) |
| Python 最小语法 | [python_for_robotics_basics](python/python_for_robotics_basics.md) |
| 读 Python ROS/RL 代码 | [robotics_Python](robotics_Python.md) |
| C++ 刷题最小语法 | [DSA_C++_Basics](DSA_C++_Basics.md) |
| 写 C++ 类/多态 | [C++_grammar_supplement](C++_grammar_supplement.md) |
| 读 C++ 控制源码 | [robotics_C++.md](robotics_C++.md) |
| 刷题方法论 | [data_stuctures_and_algorithms](data_stuctures_and_algorithms.md) |
| 树专题刷题 | [DSA_tree](DSA_tree.md) |
| 岗位/项目路线 | [Job_Requirements](Job_Requirements_for_Robot.md) |

---

## 📍 外部资源

- 刷题：[LeetCode Hot 100](https://leetcode.cn/studyplan/top-100-liked/)
- 树视频：[Bilibili 数据结构课程](https://space.bilibili.com/401399175/lists/3102780?type=season)
- ROS：[ros_logic.md](../ros_logic.md) · [ros_communication.md](../ros_communication.md)
- RL：[RL.md](../RL.md) · [edge_deployment.md](../edge_deployment.md)
- 👉 机型实战：[kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)
