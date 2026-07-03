# LLM for Robotics —— 大语言模型在机器人中的应用

> **核心定位**：在多数可落地系统中，LLM **不直接输出关节角**，而是做**高层语义理解、任务分解、规划与工具调用**。与传统 MoveIt / VLA / 行为树配合，形成 System 2（慢）+ System 1（快）分层架构。
>
> 👉 思维导图位置：[2.3.5 LLM for Robotics](../robot_system.md)
>
> 外部索引：[Embodied-AI-Guide · algorithm.md](https://github.com/TianxingChen/Embodied-AI-Guide/blob/main/topics/algorithm.md#llm_robot)

---

## 一、在系统中的位置

```
用户自然语言：「帮我把桌上工具收进抽屉」
         ↓
    LLM（System 2，~1Hz）
         ↓
  结构化计划 / 子目标 / 代码 / MCP 工具调用
         ↓
  行为树 · MoveIt · VLA · ACT/DP（System 1，10–50Hz）
         ↓
    关节动作 / 底盘运动
```

与 **VLA** 的边界：VLA 端到端输出动作；LLM 更偏「理解 + 编排」，低层交给专用 policy 或经典规划器。

---

## 二、主要范式

### 2.1 LLM 做高层规划

| 工作 | 链接 | 思路 |
|------|------|------|
| **PaLM-E** | [arXiv](https://arxiv.org/abs/2303.03378) | 多模态嵌入 + 机器人状态 |
| **EmbodiedGPT / DIAC / LBYL** | — | 具身场景 LLM 规划 |
| **LLM+P** | [arXiv](https://arxiv.org/abs/2304.11477) | LLM 生成 PDDL → 传统 planner |
| **AutoTAMP / Text2Motion** | — | 文本 → 时序逻辑 / 运动规划 |

### 2.2 3D 感知 + LLM

| 工作 | 链接 | 思路 |
|------|------|------|
| **VoxPoser** | [arXiv](https://arxiv.org/abs/2307.05973) | VLM 在 3D voxel 上生成价值场，引导 motion |
| **OmniManip** | [arXiv](https://arxiv.org/abs/2501.03841) | 3D 表征 + LLM 约束 |

### 2.3 Code as Policy / 工具调用

| 工作 | 链接 | 思路 |
|------|------|------|
| **Code as Policy (CaP)** | [arXiv](https://arxiv.org/abs/2209.07753) | LLM 生成 Python 控制代码 |
| **Instruction2Act** | [arXiv](https://arxiv.org/abs/2305.11176) | 指令 → 可执行代码片段 |

**与 Kuavo 实战对应**：

| Kuavo 实现 | 研究侧对应 |
|------------|------------|
| V1：LLM → JSON → 状态机 | LLM+P / 符号规划 |
| V2：py_trees 行为树 | 分层规划 + 可组合节点 |
| V3：MCP Tool Call | ReAct / Agent + 标准化 tool 接口 |

### 2.4 多机器人协同

| 工作 | 链接 |
|------|------|
| **RoCo** | [arXiv](https://arxiv.org/abs/2307.04738) |
| **Scalable-Multi-Robot** | [arXiv](https://arxiv.org/abs/2309.15943) |

---

## 三、LLM vs VLA vs 工程实践

| | LLM for Robotics | VLA | Kuavo VLA V1–V3 |
|--|------------------|-----|-----------------|
| **输出** | 计划 / 代码 / tool call | 连续/离散动作 | JSON / 行为树 / MCP |
| **频率** | 低（秒级） | 高（10–50Hz） | 混合 |
| **优势** | 长程推理、可解释 | 端到端、接触-rich | 工程可控、可调试 |
| **风险** | 幻觉、plan 不可执行 | 数据饥渴、黑盒 | 泛化有限 |

Embodied-AI-Guide 结论：**LLM 做高层 + VLA/IL 做低层**，是当前最可控的组合。

---

## 四、入门资源

| 资源 | 链接 |
|------|------|
| Robotics+LLM 系列（中文） | [知乎](https://zhuanlan.zhihu.com/p/668053911) |
| Lilian Weng：AI Agent | [英文](https://lilianweng.github.io/posts/2023-06-23-agent/) |
| Embodied Agent Interface（评测 LLM 决策链） | [官网](https://embodied-agent-interface.github.io/) |

---

## 五、相关专题

- [VLA 研究版图](./vla_landscape.md)
- [视觉基础模型](./vision_foundation_models.md)
- [ROS 架构逻辑 / 行为树](./ros_logic.md)
- [AI 与机器人学习拓扑](./AI_learning_robotics.md)

---

> 👉 **Kuavo 实战**：[VLA 语音抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md) · [行为树版 VLA](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) · [MCP Tool Call](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md)
