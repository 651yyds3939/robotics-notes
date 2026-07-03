# VLA 研究版图 (Vision-Language-Action Models)

> **导读**：VLA（Vision-Language-Action）是具身智能里「把看和听，直接变成动」的一类模型。研究界在 push **端到端大模型**（OpenVLA、π0）；工程界更多走 **分层系统**（LLM 规划 + YOLO/ACT 执行）——你的 Kuavo V1→V3 就是后者。本文用**流程图 + 概念 + 研究地图**把两条线都讲清楚。
>
> 👉 思维导图位置：[2.3.1 具身智能与 VLA](../robot_system.md)
>
> 外部索引：[Embodied-AI-Guide · algorithm.md](https://github.com/TianxingChen/Embodied-AI-Guide/blob/main/topics/algorithm.md#vla) · [Awesome VLA Papers](https://github.com/Psi-Robot/Awesome-VLA-Papers)

---

## 第 0 章：一句话理解 VLA

> **大白话**：给机器人一张图 + 一句「把杯子递给我」，VLA 的输出不是 JSON 计划，而是**可以直接发给电机的动作**（关节角、末端位姿、action chunk 等）。它和「LLM 只负责想、MoveIt 负责做」的分工不同，目标是**视觉-语言-动作在同一套网络里对齐**。

| 对比 | LLM for Robotics | VLA | Kuavo 工程 VLA（V1） |
|------|------------------|-----|----------------------|
| 输入 | 语言 (+ 可选图像) | 图像 + 语言 | 语音→ASR→LLM + YOLO 图像 |
| 输出 | 计划 / JSON / tool call | 动作 token / 连续 action | JSON `{"action":"grab"}` + TF2 坐标 |
| 低层执行 | MoveIt / 状态机 / MCP | 模型内部 action head | IK + 守护进程 + WBC |
| 频率 | ~1Hz | 10–50Hz（目标） | 混合：LLM 慢、抓取链快 |

---

## 第 1 章：VLA 机器人系统通用架构图（概念数据流）

> 适用于理解 OpenVLA、Octo、π0 等**研究型 VLA**，也适用于分析任意具身系统的模块划分。与 Kuavo 9 终端实机图对照阅读效果更佳。

```text
========================================================================================================
                         🤖 VLA 机器人系统通用架构（Vision-Language-Action Pipeline）
========================================================================================================

  [ 人类 / 任务源 ]
       |  自然语言指令：「把桌上的水瓶递给我」
       |  （可选）演示视频 / 遥操作轨迹（训练阶段）
       v
========================================================================================================
  [ 传感器层 · Sensors ]
========================================================================================================
       |                    |                      |
       | RGB / RGB-D 相机    | 本体感知 Proprio      | 可选：触觉 / 力矩 / 语言 token
       | (多视角)            | 关节角·IMU·夹爪状态    |
       v                    v                      v
========================================================================================================
  [ 感知编码层 · Perception Encoding ]                    👉 [视觉基础模型专题](./vision_foundation_models.md)
========================================================================================================
       |                    |
       | 视觉 backbone       | 语言 encoder
       | ViT / ResNet /      | 文本 embedding /
       | 冻结 CLIP 特征      | 指令 token 序列
       v                    v
       +---------+----------+
                 |
                 v
========================================================================================================
  [ 融合层 · Multimodal Fusion ]  （单模型 VLA 内部完成；工程系统可能在 LLM 处融合）
========================================================================================================
                 |
       +---------+---------+
       |  【路径 A：端到端 VLA】          |  【路径 B：工程分层（Kuavo 类）】
       |  视觉+语言 joint attention       |  System 2: LLM/VLM 出 JSON/子目标
       |  → 统一 latent 表征              |  System 1: YOLO/ACT 出坐标/轨迹
       +---------+---------+
                 |
                 v
========================================================================================================
  [ 动作层 · Action Head ]  ⭐ VLA 的核心差异点
========================================================================================================
                 |
       +---------+---------+---------+
       | Autoregressive     | Diffusion / Flow  | 离散 skill token
       | (RT-1/2, OpenVLA)  | (Octo, π0, DP)    | (高层宏动作)
       | action token 序列   | 连续动作分布采样    |
       v                    v                    v
       +---------+----------+-------------------+
                 |
                 |  输出：action chunk（未来 H 步）
                 |        Δq / 末端位姿 / 夹爪开合 / 底盘 twist
                 |        典型频率：10 ~ 50 Hz
                 v
========================================================================================================
  [ 低层控制与安全 · Low-level Control ]  （几乎总是经典控制，很少被 VLA 完全替代）
========================================================================================================
                 |
       | IK / 轨迹插值 / MoveIt 避障
       | WBC / MPC / 阻抗控制（人形 100~1000 Hz）
       | 软限位 · 碰撞检测 · 急停
                 v
========================================================================================================
  [ 执行层 · Actuators ]  电机 · 夹爪 · 轮足底盘
========================================================================================================

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  训练闭环（离线，非实机运行时）                                           │
  │  Dataset (Open X-Embodiment / DROID / 自采 LeRobot)                     │
  │       → 预训练 VLA 或 IL fine-tune → 评测 Benchmark (LIBERO/RoboTwin…)   │
  │  👉 [Benchmark 与 Dataset 专题](./benchmark_dataset.md)                 │
  └─────────────────────────────────────────────────────────────────────────┘
```

### 1.1 流程图导读

1. **纵向**：从人类指令 → 传感器 → 感知编码 → 融合 → **动作头** → 低层控制 → 电机，与 [机器人全链路思维导图](../robot_system.md) 的「感知→决策→控制→执行」一一对应。
2. **路径 A vs B**：研究 VLA 走 A（单模型）；Kuavo V1/V2/V3 走 B（分层），**本质仍是 VLA 系统**，只是动作头被拆成 LLM + YOLO + IK。
3. **动作层是分水岭**：VLA 论文的创新点多半在「怎么把连续控制量表示成可学习的 token / diffusion 目标」。

---

## 第 2 章：研究型端到端 VLA 数据流（OpenVLA / Octo 类）

```text
========================================================================================================
                    📚 研究型端到端 VLA 推理流程（单模型 · 无显式状态机）
========================================================================================================

  [ 相机图像 I_t ]  +  [ 语言指令 L ]  +  [ 可选：机器人状态 q_t ]
            \              |                    /
             \             |                   /
              v            v                  v
         ┌────────────────────────────────────────┐
         │     VLA Backbone (ViT + LLM trunk)       │
         │     OpenVLA-7B / Octo-93M / π0-3.3B      │
         └────────────────────┬───────────────────┘
                              │
                              v
         ┌────────────────────────────────────────┐
         │     Action Head                          │
         │     · AR: 逐个预测 discretized action    │
         │     · Diffusion: 去噪采样 action chunk   │
         │     · Flow: π0 FAST tokenizer            │
         └────────────────────┬───────────────────┘
                              │
                              v
                    a_t, a_{t+1}, …, a_{t+H}
                    （14~32 维 joint / EE delta）
                              │
                              v
                    [ 真机 / 仿真 low-level PD ]
                              │
                              v
                         任务成功率 @ Benchmark

  训练数据：Open X-Embodiment / Bridge / 自采 demo
  评测：SimplerENV / LIBERO / 真机成功率
  特点：换任务靠 prompt / fine-tune，不靠手写 if-else
```

**你需要自己训练吗？**

| 场景 | 做法 |
|------|------|
| 复现论文 | 下载 **OpenVLA / Octo / openpi 预训练权重**，在 benchmark 上评测 |
| 换机器人 / 新任务 | **Fine-tune**（LoRA 或全参），需自有或公开 demo 数据 |
| 从零预训练 VLA | 仅大厂/实验室；个人/项目 **不推荐** |

---

## 第 3 章：2025 分层双系统 VLA 架构图

```text
========================================================================================================
              🧠 分层双系统 VLA（System 2 慢思考 + System 1 快执行）— 2025 主流产业路线
========================================================================================================

  用户：「先把乱了的工具收进抽屉，再把水瓶递给我」
       |
       v
  ┌─────────────────────────────────────────────────────────────┐
  │  System 2 · 慢系统 (~0.5–2 Hz)                               │
  │  VLM / LLM：Gemini Robotics · GO-1 ViLLA · Hi-Robot VLM    │
  │  · 长程任务分解 → 子目标序列 / latent plan / 语言子指令       │
  └────────────────────────────┬────────────────────────────────┘
                               │ 子目标：「定位水瓶」→「抓取」→「递给人类」
                               v
  ┌─────────────────────────────────────────────────────────────┐
  │  System 1 · 快系统 (~20–50 Hz)                               │
  │  VLA / IL：GR00T-N1 · π0 · ACT · Diffusion Policy            │
  │  · 每步子目标 → 连续 action chunk                             │
  └────────────────────────────┬────────────────────────────────┘
                               v
  ┌─────────────────────────────────────────────────────────────┐
  │  经典控制兜底 (~100–1000 Hz)  WBC / IK / 安全限幅              │
  └────────────────────────────┬────────────────────────────────┘
                               v
                         物理机器人

  代表：Figure Helix · 智元 GO-1 · NVIDIA GR00T-N1 · Physical Intelligence π0.5
  与 Kuavo 关系：你的 V2 行为树 + V3 MCP ≈ System 2；ACT/YOLO+IK ≈ System 1
```

---

## 第 4 章：Kuavo 工程 VLA 实机架构图（对照 22.1）

> 完整终端命令与踩坑见 kuavo-dev-notes：**[22.1 VLA 视听觉全闭环抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md)**。下图与 22.1 同源，便于在通用笔记里建立「工程 VLA ≠ 论文 VLA，但是同一套分层思想」的认知。

```text
========================================================================================================
              🦾 Kuavo VLA V1 工程架构（9 终端 · 脑手分离 · 非端到端大模型）
========================================================================================================

  [ 外设 ]  🎤 USB 麦克风（远离风扇）   👀 RealSense RGB-D   🔊 板载喇叭
       |              |                      |
       v              v                      v
========================================================================================================
  [ 阵列三 · 上位机 Jetson Orin NX · 192.168.26.12 ]  GPU：视觉 + 大模型
========================================================================================================
       |                              |
[终端 9] VLA 主控 (rtasr_python3_demo)  [终端 6] 相机 launch
       |                              [终端 7] YOLO+TF2 (yolo_TF2.py)
       |-- VAD 端点检测                  |-- COCO yolov8n-seg · 过滤 bottle
       |-- ASR (Faster-Whisper)          |-- TF2 → /vla/yolo_target
       |-- LLM (Qwen2-7B) 意图提取       |
       |-- JSON: {action, target}        |
       |-- TTS 反馈                      |
       |                              [终端 8] rqt 监视
=======|==============================|================================================
       |   ROS / HTTP 跨 192.168.26.x 局域网
=======|==============================|================================================
       v                              v
========================================================================================================
  [ 阵列二 · 下位机 NUC · lab 用户 ]  调度 + 发声 + 抓取守护
========================================================================================================
[终端 4] TTS Server (lab 用户!)    [终端 5] vla_auto_grasp_daemon.py
       |                              |-- 订阅 JSON + TF2 坐标
       |-- VITS 离线合成                 |-- 滤波 · 关节空间大展翅避障
       v                              |-- 下发 14 轴轨迹
  物理发声                             v
========================================================================================================
  [ 阵列一 · 下位机 NUC · root ]  运动底层
========================================================================================================
[终端 1] WBC load_kuavo_real.launch (1kHz)
[终端 2] IK ik_node.launch
[终端 3] look_down.py 锁头 TF 基准
       |
       v
  🤖 机械臂 + Leju 夹爪

  ┌─ 这在 VLA 谱系里算什么？ ─────────────────────────────────────────┐
  │  System 2：ASR + LLM → JSON 意图（不是 RT-2 那种 action token）     │
  │  感知：YOLO COCO 预训练（不是 VLM end-to-end）                      │
  │  System 1：IK + 守护状态机（不是 Diffusion Policy 端到端）           │
  │  结论：工程可落地、可调试；研究 metrics 上不算「纯 VLA 模型」         │
  └────────────────────────────────────────────────────────────────────┘
```

### 4.1 Kuavo V1 → V2 → V3 演进（同一流程图的三种 System 2）

| 版本 | System 2 变化 | 抓取执行链 |
|------|--------------|-----------|
| **V1** | LLM → JSON → **硬编码状态机**（9 终端） | YOLO+TF2 → daemon → IK → WBC |
| **V2** | LLM → **py_trees 行为树**（可组合节点） | 同上 👉 [22.2 行为树版](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) |
| **V3** | LLM → **MCP Tool Call**（detect/grasp/speak） | HTTP 桥 + 同上 👉 [22.3 MCP](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md) |

**IL 路线（平行于 V1–V3 语言链）**：LeRobot 采 demo → ACT / Diffusion Policy 训 System 1 → 真机部署 👉 [8. 模仿学习](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/8.imitation_learning.md) · [22.4 数据采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md)

---

## 第 5 章：VLA 三个关键设计（读论文时抓这三条）

### 5.1 动作表示 (Action Representation)

连续关节角不能直接喂给 LLM，必须「可 token 化」：

| 方法 | 代表 | 直觉 |
|------|------|------|
| **均匀离散化** | RT-1 | 把每个关节角区间切成 bins → 词表 token |
| **FAST tokenizer** | π0 | 学一个压缩动作序列的 codec |
| **Diffusion / Flow** | Octo, DP | 不离散化，直接生成连续 action 向量 |
| **Latent action** | GO-1, UniVLA | System 2 输出 latent，System 1 解码 |

### 5.2 训练数据

| 类型 | 代表 | 特点 |
|------|------|------|
| 跨本体大规模 | Open X-Embodiment | OpenVLA/Octo 基础 |
| 单实验室 | DROID, Bridge | 真实 teleop |
| 仿真合成 | RoboTwin, MimicGen | 规模化、便宜 |
| 自采 | Kuavo LeRobot | 单本体、任务特化 |

### 5.3 系统形态

| 形态 | 优点 | 缺点 |
|------|------|------|
| **单模型端到端** | 简洁、可 end-to-end fine-tune | 黑盒、难插安全约束 |
| **分层双系统** | 可解释、易工程兜底 | 模块多、接口要对齐 |
| **工程分层（Kuavo）** | 可调试、实机验证快 | 论文 novelty 低、泛化靠规则 |

---

## 第 6 章：演进时间线

| 时间 | 工作 | 要点 | 链接 |
|------|------|------|------|
| 2022 | **RT-1** | Transformer 离散 action token | [arXiv](https://arxiv.org/abs/2212.06817) |
| 2023 | **RT-2** | VLM 知识注入；55B | [arXiv](https://arxiv.org/abs/2307.15818) |
| 2024 | **OpenVLA** | 7B 开源；OXE 数据 | [GitHub](https://github.com/openvla) |
| 2024 | **Octo** | 93M；Diffusion head | [GitHub](https://github.com/octo-models/octo) |
| 2024 | **π0** | Flow + FAST | [openpi](https://github.com/Physical-Intelligence/openpi) |
| 2024 | **RDT-1B** | 双臂 Diffusion Transformer | [GitHub](https://github.com/thu-ml/RoboticsDiffusionTransformer) |
| 2025 | **GR00T-N1 / GO-1 / π0.5** | 分层双系统 + 全身/移动 | 见 §3 架构图 |

---

## 第 7 章：按动作头分类（研究选型）

| 类型 | 代表 | 链接 |
|------|------|------|
| **Autoregressive** | RT-1/2、OpenVLA、RoboFlamingo | [OpenVLA](https://github.com/openvla) |
| **Diffusion / Flow** | Octo、π0、RDT-1B、Diffusion Policy | [openpi](https://github.com/Physical-Intelligence/openpi) · [DP](https://github.com/real-stanford/diffusion_policy) |
| **3D 增强** | 3D-VLA、SpatialVLA、DP3 | [DP3](https://github.com/YanjieZe/3D-Diffusion-Policy) |
| **跨场景** | NaVILA、Mobility-VLA、QUAR-VLA | [NaVILA](https://navila-bot.github.io/) |

**工程 IL 基线**（常作 System 1，非完整 VLA）：

| 基线 | 链接 | 说明 |
|------|------|------|
| **ACT** | [GitHub](https://github.com/tonyzhaozh/act) | RoboTwin 教程默认 baseline |
| **Diffusion Policy** | [GitHub](https://github.com/real-stanford/diffusion_policy) | 接触-rich 操作稳健 |

---

## 第 8 章：人形 / 移动相关 VLA

| 工作 | 场景 | 与 Kuavo 关系 |
|------|------|--------------|
| **NaVILA** | 腿式 + 语言导航 | 语言控行走，非抓取 |
| **GR00T-N1** | 全身操作 | 人形 upper-body VLA 参考 |
| **Mobility-VLA** | 移动导航 | 底盘 + 语义 |
| **RDT-1B** | 双臂桌面 | 上肢操作 IL/VLA |

人形完整 VLA（走+抓+说）尚无统一开源端到端方案；**locomotion 仍多为 RL（Isaac Lab）**，**操作多为 IL/VLA 分层**，与 Kuavo 现状一致。

---

## 第 9 章：自己训练 VLA 还是调用预训练？

| 路径 | 何时选 | 成本 |
|------|--------|------|
| **调用 OpenVLA/Octo/openpi 权重** | 复现 benchmark、同构机械臂 | 低 |
| **Fine-tune（LoRA）** | 自有 LeRobot 数据、新任务 | 中；需 GPU 集群 |
| **只训 System 1（ACT/DP）** | Kuavo 抓取；LLM 仍用 Qwen | 中；工程最常见 |
| **从零预训练 VLA** | 基本不做 | 极高 |

**Kuavo 推荐路径**：V1–V3 语言链（零训练 LLM 推理）+ YOLO 预训练 + 可选 ACT/DP fine-tune on LeRobot；**不必**强行上 OpenVLA-7B 除非要做 research baseline。

---

## 第 10 章：常见误区

| 误区 | 正解 |
|------|------|
| 「做了语音抓取就是 VLA 论文」 | 工程 VLA 系统 ≠ 端到端 VLA **模型** |
| 「VLA 要替代 WBC/IK」 | 低层控制几乎总在；VLA 输出多被 IK/WBC 兜底 |
| 「必须上大 VLA 才能抓水瓶」 | COCO YOLO + IK 已够；见 [4.3](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.3.real_robot_yolo_environment.md) |
| 「VLA 和 LLM 机器人二选一」 | 2025 趋势是 **LLM/VLM 做 System 2 + VLA/IL 做 System 1** |

---

## 第 11 章：综述与动手入口

| 资源 | 链接 |
|------|------|
| VLA Survey (Action Tokenization) | [arXiv](https://arxiv.org/abs/2507.01925) |
| VLA for Embodied AI Survey | [arXiv](https://arxiv.org/abs/2405.14093) |
| Embodied-AI-Guide 动手教程 | [RoboTwin 2.0 + ACT](https://github.com/TianxingChen/Embodied-AI-Guide#robotwin) |

---

## 第 12 章：相关专题

- [LLM for Robotics](./llm_for_robotics.md) — System 2 / MCP / 行为树
- [视觉基础模型](./vision_foundation_models.md) — YOLO vs VFM
- [Benchmark 与 Dataset](./benchmark_dataset.md) — 训练与评测数据
- [AI 与机器人学习拓扑](./AI_learning_robotics.md) — IL / RL / LLM 分工

---

> 👉 **Kuavo 实战全系列**：
> [22.1 VLA 九终端架构](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.1VLA_grasping.md) ·
> [22.2 行为树版](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md) ·
> [22.3 MCP](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.3.MCP_VLA_grasp.md) ·
> [22.4 LeRobot 采集](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.4.Lerobot_grasp.md) ·
> [8. 模仿学习](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/8.imitation_learning.md)
