# 视觉基础模型 (Vision Foundation Models)

> **导读**：如果说 YOLO 是机器人视觉里「反应最快的前哨侦察兵」，那 Vision Foundation Models（VFM，视觉基础模型）更像是「读过海量互联网图文的通用眼睛」——它们不一定直接告诉你电机怎么转，但能把复杂世界压缩成语义一致、可泛化、可和语言对齐的中间表示，供下游抓取、导航、VLA 使用。
>
> 👉 思维导图位置：[1.4 高层感知算法](../robot_system.md)
>
> 外部索引：[Embodied-AI-Guide · algorithm.md](https://github.com/TianxingChen/Embodied-AI-Guide/blob/main/topics/algorithm.md#foundation-models)

---

## 第 0 章：一句话理解 VFM

> **大白话**：VFM 是在**超大规模数据**（互联网图像、图文对、视频等）上预训练出来的视觉模型。它们学到的不是「只会认 80 类 COCO 物体」，而是一种**通用的视觉理解能力**——分割、对齐、深度、对应关系等。在机器人里，你通常**直接调用别人训好的权重**，而不是从零自己训练。

| 维度 | 传统检测器（YOLO） | 视觉基础模型（VFM） |
|------|-------------------|---------------------|
| 训练数据规模 | COCO 等百万级标注 | 常是十亿级图文 / 自监督 |
| 输出 | 固定类别 bbox / mask | 特征 / 开放词表检测 / 提示分割 / 深度等 |
| 换目标物体 | 改类别过滤，或重新标注微调 | 改文本提示 / 点框提示，Often 零样本 |
| 部署难度 | 低（单模型、单 API） | 中～高（常需多模型 pipeline） |
| 典型延迟 | 实时（30–100+ FPS） | 多数更重（取决于模型大小） |

---

## 第 1 章：VFM 在机器人系统中的位置

```
相机 RGB / Depth
    ↓
【感知层】Vision Foundation Models / YOLO / 经典 CV
    ↓
检测框 · 分割 mask · 深度图 · 6D 位姿 · 语义特征
    ↓
【决策层】LLM 规划 · VLA · MoveIt · 行为树
    ↓
【控制层】IK / WBC / RL
    ↓
关节动作
```

**关键结论**：VFM 和 YOLO 都工作在**感知层**，都不直接输出关节角。区别是 YOLO 偏「固定任务、低延迟检测」；VFM 偏「开放世界、语言/提示驱动、更强泛化」。

---

## 第 2 章：概念辨析——YOLO、预训练检测、VFM 不是一回事

很多人把「用了深度学习」都叫 AI 视觉，但在工程上至少要分三层：

### 2.1 YOLO 家族（任务专用检测器）

- **本质**：为**目标检测**（+ 可选分割）设计的卷积/Transformer 网络。
- **典型权重**：`yolov8n.pt`、`yolov8n-seg.pt`，在 **COCO 80 类**上预训练。
- **用法**：`model(image)` → 得到 `boxes`、`scores`、`class_names`。
- **「开箱即用」程度**：⭐⭐⭐⭐⭐（`pip install ultralytics` 即可）。

### 2.2 预训练检测模型 ≠ VFM

你在 Kuavo **4.3** 里用的 `yolov8n-seg.pt` 属于：

> **「别人训好的 COCO 通用检测/分割权重 + 自己写业务过滤逻辑」**

例如过滤 `class_name == 'bottle'`，这就是**直接调用预训练模型**，**不需要自己从零训练**。但它仍然是 YOLO 路线，不是 VFM 路线——因为类别空间被 COCO 的 80 类锁死了。

### 2.3 Vision Foundation Models（视觉基础模型）

- **本质**：在大规模数据上学**通用视觉表征**，再适配多种下游任务。
- **典型能力**：
  - **图文对齐**（CLIP）：图像和文本进同一语义空间；
  - **提示分割**（SAM）：给点/框 → 出 mask，不依赖固定类别表；
  - **开放词表检测**（Grounding-DINO）：给文本 → 出框；
  - **单目深度**（Depth Anything）：RGB → 深度图；
  - **6D 位姿**（FoundationPose）：已知 mesh 的物体位姿追踪。
- **「开箱即用」程度**：⭐⭐⭐～⭐⭐⭐⭐（单模型可跑，但机器人 pipeline 常要组合 2～3 个模型）。

### 2.4 对照表（帮你选型时不混淆）

| 问题 | YOLO + COCO 预训练 | VFM |
|------|-------------------|-----|
| 抓 COCO 里的 `bottle` / `cup` | ✅ 足够，且更快 | 大材小用 |
| LLM 说「抓螺丝刀」且 COCO 无此类 | ❌ 需换类名或微调 | ✅ Grounding-DINO / YOLO-World |
| 只要 bbox，要 30Hz+ | ✅ YOLO 首选 | 通常偏慢 |
| 要精确物体轮廓（mask） | `yolov8-seg` 可以 | SAM 往往更精细 |
| 只有 RGB、没有深度相机 | 需 Depth Anything 等补深度 | ✅ |
| 中文「水瓶」直接驱动检测 | 需自建「中文→COCO类名」映射 | 文本 prompt 更自然 |

---

## 第 3 章：自己训练 vs 直接调用预训练模型？

这是机器人工程里最高频的问题。结论先行：

> **99% 的机器人视觉项目应优先「调用别人训好的预训练模型 + 写业务逻辑」；只有预训练搞不定时才考虑微调或自训。**

### 3.1 四条路径（按推荐顺序）

| 路径 | 做什么 | 何时选 | 成本 |
|------|--------|--------|------|
| **A. 零训练推理** | 下载 `.pt` / HuggingFace 权重，直接 `predict` | 目标在 COCO 80 类内，或 VFM 零样本可用 | 最低 |
| **B. 业务逻辑封装** | 类名过滤、阈值、ROI、TF、IK（你的 4.3 就在这层） | 几乎总是需要 | 低 |
| **C. 微调 (Fine-tune)** | 在自己的图像上继续训练若干 epoch | 工厂特定零件、光照极端、COCO 认不准 | 中 |
| **D. 从零训练** | 自己标注数据、定义类别、训检测器 | 极少需要；除非保密场景+海量专有数据 | 高 |

### 3.2 你**不需要**自己训练的情况（优先预训练）

- 抓**水瓶、杯子、人、椅子**等 COCO 常见类 → **YOLO COCO 权重 + 过滤**（你的 4.3 方案）；
- 需要**单目深度**、没有 RealSense → **Depth Anything 预训练**；
- 需要**「文本描述物体」**且不想标注 → **Grounding-DINO / YOLO-World 预训练**；
- 需要**分割 mask** → **SAM2 预训练**（用检测框当初始 prompt）；
- 做 VLA/IL 的**感知前端** → 多数论文也是 **冻结或微调** 预训练 backbone，而非从零训。

### 3.3 你**可能需要**微调或自训的情况

- **工业专有零件**（某型号螺丝、某品牌工装），COCO/VFM 都认不出；
- **极端域**：强反光、透明纯玻璃、强粉尘，预训练置信度长期 `< 0.15`；
- **固定工位 + 固定 SKU 很少**：标注 500～2000 张，YOLO 微调往往比上大 VFM 更划算；
- **latency 极限优化**：把大 VFM 蒸馏成小 YOLO（高级玩法，后期再做）。

### 3.4 决策流程图（可直接当 checklist）

```
目标物体是什么？
    │
    ├─ 在 COCO 80 类里（bottle/cup/person…）
    │       → 用 yolov8n-seg.pt 等预训练 + 类名过滤  【Kuavo 4.3 路线】
    │
    ├─ 不在 COCO，但能用语言描述
    │       → Grounding-DINO / YOLO-World 预训练 + 文本 prompt
    │
    ├─ 需要精细 mask / 遮挡严重
    │       → 检测器 + SAM2 预训练 pipeline
    │
    ├─ 只有 RGB、要 3D
    │       → Depth Anything 预训练 + 点云/IK
    │
    └─ 以上都失败、且有标注预算
            → YOLO 微调（优先）→ 仍不行再考虑 VFM 微调
```

### 3.5 「训练」在机器人项目里通常指什么？

| 说法 | 实际含义 |
|------|----------|
| 「训练 YOLO」 | Often 指 **fine-tune**：在 COCO 预训练权重上，用自有标注继续训 |
| 「训练 VFM」 | 几乎总是 **调用 checkpoint**；全量预训练只有大厂做得起 |
| 「训练 VLA」 | 训的是**策略网络**（视觉→动作），感知 backbone 常冻结预训练 ViT |
| 「训练 RL」 | 训 locomotion policy，和「训练检测器」是另一条线 |

---

## 第 4 章：YOLO vs VFM——与 Kuavo 4.3 实战对照

你在 [4.3 YOLOv8 真机部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.3.real_robot_yolo_environment.md) 里已经走通的是**预训练 YOLO 路线**，不是 VFM，但工程上完全正确：

| 环节 | 你的 4.3 做法 | 属于哪类 |
|------|--------------|----------|
| 模型 | `yolov8n-seg.pt`（COCO 预训练） | 调用别人训好的权重 ✅ |
| 指定水瓶 | 过滤 `bottle` / `cup` | 业务逻辑，非再训练 ✅ |
| 3D | RealSense 深度 + 中值滤波 + TF2 | 经典几何，非学习 ✅ |
| MCP `locate_target_yolo("水瓶")` | `object_name` 预留语义；检测仍靠 COCO 类 | LLM 层中文 ↔ 检测层英文类名，**尚未 open-vocab** |

**何时从 4.3 升级到 VFM？**

- LLM 说「抓螺丝刀 / 苹果 / 遥控器」，不想每次改 `if class_name == ...`；
- 希望 **中文 object_name 直接驱动检测**，不做 COCO 类名映射表；
- 透明瓶、反光导致 YOLO+深度不稳定，想试 **SAM mask + 更稳的 ROI**（4.3 已用垫高、材质优选等工程手段，VFM 是备选而非必须）。

**若升级，最小改动建议**：

1. **仍要 YOLO 体验**：试 **YOLO-World**（Ultralytics API 几乎不变，加 `set_classes(["水瓶","bottle"])`）；
2. **要语言 open-vocab**：**Grounding-DINO** 替换检测头，后面 TF→IK 不变；
3. **只要更好 mask**：保留 YOLO 框，后接 **SAM2**  refine 分割区域。

---

## 第 5 章：VFM 能力地图（预训练可直接用的代表）

> 下列模型均指 **下载官方权重即可推理**；机器人项目里极少需要从头预训练。

### 5.1 图文对齐（语言 ↔ 视觉）

| 模型 | 链接 | 预训练用途 | 是否常自训 |
|------|------|-----------|-----------|
| **CLIP** | [GitHub](https://github.com/openai/CLIP) | 图文相似度、粗筛目标 | ❌ 直接调用 |
| **SigLIP** | [HF](https://huggingface.co/docs/transformers/en/model_doc/siglip) | CLIP 改进版 | ❌ 直接调用 |

### 5.2 表征学习（correspondence / 跨帧）

| 模型 | 链接 | 预训练用途 | 是否常自训 |
|------|------|-----------|-----------|
| **DINO v2/v3** | [GitHub](https://github.com/facebookresearch/dino) | 特征匹配、跟踪、分割 prompt | ❌ 直接调用 |

### 5.3 分割（哪里是物体 / 可操作区域）

| 模型 | 链接 | 预训练用途 | 是否常自训 |
|------|------|-----------|-----------|
| **SAM / SAM2** | [官网](https://segment-anything.com) | 点/框 → mask | ❌ 直接调用 |
| **Grounded-SAM** | [GitHub](https://github.com/IDEA-Research/Grounded-SAM-2) | 文本 → 框 → mask | ❌ pipeline 组合 |

### 5.4 开放词表检测（最接近「语言版 YOLO」）

| 模型 | 链接 | 预训练用途 | 是否常自训 |
|------|------|-----------|-----------|
| **YOLO-World** | [Ultralytics](https://docs.ultralytics.com/models/yolo-world/) | 文本指定类别，YOLO 式 API | ❌ 直接调用 |
| **Grounding-DINO** | [GitHub](https://github.com/IDEA-Research/GroundingDINO) | 文本 → bbox | ❌ 直接调用；极少微调 |
| **OWL-ViT v2** | [HF](https://huggingface.co/docs/transformers/model_doc/owlv2) | 文本查物体 | ❌ 直接调用 |

### 5.5 几何 / 3D

| 模型 | 链接 | 预训练用途 | 是否常自训 |
|------|------|-----------|-----------|
| **Depth Anything v2** | [GitHub](https://github.com/LiheYoung/Depth-Anything) | 单目深度 | ❌ 直接调用 |
| **FoundationPose** | [GitHub](https://github.com/NVlabs/FoundationPose) | 6D 位姿（需物体 mesh） | ❌ 直接调用；配置成本高 |
| **Point Transformer v3** | [GitHub](https://github.com/Pointcept/PointTransformerV3) | 点云特征 | 研究向；工程少自训 |

---

## 第 6 章：典型工程管线（均基于预训练，非自训）

| 任务 | 推荐 pipeline | 训练需求 |
|------|---------------|----------|
| 固定类抓取（水瓶） | YOLO COCO + `bottle` 过滤 → 深度 → TF → IK | **零训练**（4.3） |
| 语言指定物体 | Grounding-DINO → 深度 → TF → IK | **零训练** |
| 语言 + 精细 mask | Grounding-DINO → SAM2 → 深度 → IK | **零训练** |
| 无 RGB-D | Depth Anything → 伪点云 → 规划 | **零训练** |
| 已知 CAD 的工业件 | FoundationPose + mesh | **零训练**；需 3D 资产 |
| 工厂独有零件 | 标注 500+ 张 → YOLO **微调** | **仅微调** |

---

## 第 7 章：性能与部署权衡（Orin / 工控机视角）

| 方案 | 相对延迟 | Orin NX 可行性 | 备注 |
|------|----------|----------------|------|
| YOLOv8n | 最快 | ✅ 40–60ms/帧（4.3 实测） | 固定类首选 |
| YOLOv8n-seg | 快 | ✅ | 带 instance mask |
| YOLO-World | 中 | ✅ 需实测 | API 与 YOLO 接近 |
| Grounding-DINO tiny | 中～慢 | ⚠️ 需实测 | open-vocab |
| SAM2 base | 慢 | ⚠️ 常作 refine 非每帧全图 | 可与 YOLO 框级联 |
| Depth Anything v2 small | 中 | ✅ | 无深度相机时 |

**工程原则**：感知链路的延迟会传导到抓取闭环；**没有 open-vocab 需求时，不要为了「更先进」牺牲 YOLO 的稳定性**。

---

## 第 8 章：常见误区

| 误区 | 正解 |
|------|------|
| 「做机器人视觉都要自己训模型」 | 多数项目 **调用 COCO/VFM 预训练 + 业务逻辑** 即可 |
| 「VFM 可以完全替代 YOLO」 | 对固定类、高帧率任务，YOLO 往往更合适 |
| 「用了 yolov8n-seg.pt 就是 VFM」 | 仍是 **YOLO + COCO 预训练**；VFM 指 CLIP/SAM/Grounding-DINO 等另一生态 |
| 「MCP 传了中文 object_name，检测就是 open-vocab」 | 除非检测节点接文本模型，否则仍靠 **COCO 类名过滤** |
| 「检测不准就加大模型」 | 先查 **光照、垫高、材质、深度噪点、标定**（4.3/4.4 血泪经验） |

---

## 第 9 章：相关专题与实战

- [AI 与机器人学习拓扑](./AI_learning_robotics.md) — DL / IL / VLA 在系统中的分工
- [相机标定](./camera_calibration.md) — 手眼标定是抓取前提
- [VLA 研究版图](./vla_landscape.md) — 感知之后如何到动作
- [LLM for Robotics](./llm_for_robotics.md) — 中文指令如何接到工具链

👉 **Kuavo 实战**：
- [4.3 YOLOv8 真机部署（COCO + bottle）](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.3.real_robot_yolo_environment.md)
- [4.4 TF2 视觉抓取闭环](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.4real_visual_grasp.md)
- [VLM 图像触发](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/30.AI_image_identification.md)
