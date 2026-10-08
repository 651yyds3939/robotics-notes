# 边缘端模型部署 —— ONNX / TensorRT 方法与验证清单

> **核心定位**：机器人可以直接使用 PyTorch 推理，也可以选择 ONNX Runtime 或 TensorRT；应按模型、硬件、资源和控制周期实测选型，不能预设导出后一定更小或更快。
>
> **成果边界**：下文是部署方法笔记；已有 Kuavo ONNX 实验见链接。TensorRT、FP16 和 INT8 部分不代表已经完成本人的板端性能验收。
>
> 👉 实战笔记：[RL Sim2Real ONNX 部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md)

---

## 第 0 章：边缘部署一句话

> **一句话**：从 [RL 策略](./RL.md) checkpoint 中提取推理所需的网络、权重及预处理配置，在目标 NUC/Orin 上验证数值一致性、闭环行为与延迟。Checkpoint 可能包含优化器和训练状态；ONNX 格式转换不等于压缩，也不能保证 1 ms 推理。

---

## 第 1 章：ONNX —— 通用的模型交换格式

### 1.1 导出流程

```python
import torch

# 加载训练好的 PyTorch checkpoint
checkpoint = torch.load("model_4000.pt", map_location="cpu")
actor_state = checkpoint["actor_state"]

# 构建一个干净的网络实例，加载权重
policy = ActorCritic(...).actor
policy.load_state_dict(actor_state)
policy.eval()

# 定义虚构的输入尺寸（必须和训练时的 obs 维度一致）
dummy_input = torch.randn(1, 115) # S49 舞蹈: 115维观测

# 导出 ONNX
torch.onnx.export(
 policy,
 dummy_input,
 "kuavo_policy.onnx",
 input_names=["observations"],
 output_names=["actions"],
 opset_version=11, # 兼容性关键参数
 dynamic_axes=None # 固定 batch=1，不要动态轴
)
```

### 1.2 ONNX 验证

```python
import onnx, onnxruntime
import numpy as np

# 验证 ONNX 模型结构完整性
model = onnx.load("kuavo_policy.onnx")
onnx.checker.check_model(model)

# 对比推理精度：ONNX vs PyTorch 针对同一输入
ort_session = onnxruntime.InferenceSession("kuavo_policy.onnx")
onnx_output = ort_session.run(None, {"observations": dummy_input.numpy()})[0]
with torch.no_grad():
    torch_output = policy(dummy_input).cpu().numpy()

assert np.allclose(onnx_output, torch_output, atol=1e-5), "精度不匹配！"
```

这是承接上一段已初始化 `policy` 的示例，不是独立可运行脚本。应另外用代表性观测批次测试最大误差、平均误差、非有限输出和闭环表现；单个随机输入相近不能证明策略部署安全。

---

## 第 2 章：TensorRT —— NVIDIA 的推理加速器

TensorRT 是 NVIDIA 的推理优化引擎，对 ONNX 模型做图优化、层融合、精度量化。

| 优化方式 | 原理 | 潜在收益 | 验证要求 |
|----------|------|------------|---------|
| **FP16** | 半精度浮点 | 可能减少存储并提高部分 GPU 上的速度 | 验证算子支持、数值误差与闭环表现 |
| **INT8** | 8-bit 整数量化 | 可能降低内存和计算成本 | 根据量化流程使用代表性校准数据或显式量化参数，并做精度回归 |
| **Layer Fusion** | 合并可融合的相邻算子 | 可能减少访存和调度开销 | 依模型和后端测量，数值结果仍需验证 |

不使用通用的“翻倍”或“3–4 倍”作为项目指标。记录具体模型、运行时版本、功耗模式、batch、warm-up、P50/P95/P99 及端到端延迟。FP16 的收益和误差均依模型与设备而异，参见 [ONNX Runtime 官方说明](https://onnxruntime.ai/docs/performance/model-optimizations/float16.html)。

### 2.1 导出 TensorRT Engine

```bash
# 先核对目标机的 TensorRT 版本和支持的参数；以下为常见版本示例
trtexec --help
trtexec --onnx=kuavo_policy.onnx \
 --saveEngine=kuavo_policy.trt \
 --fp16
```

旧版本的 `--workspace` 与新版本的内存池参数不能直接混用；精度选项也应以本机 `--help` 和对应版本官方文档为准。Engine 不应默认视为跨 GPU、TensorRT 或 JetPack 版本可移植。

参考 [NVIDIA TensorRT 性能基准官方文档](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html)；实际命令应使用与目标设备安装版本一致的文档。

### 2.2 Orin NX 部署注意

- Orin NX 的 GPU 显存和 CPU 内存**物理共享**（Unified Memory），模型不能太大
- 对 FP32/FP16 等候选方案分别实测精度、时延、内存和功耗，不能预设 FP16 最优或必然翻倍
- 显存告急时用 `jtop` 实时监控，关掉 GUI 和 `rqt` 等吃显存的进程

---

## 第 3 章：Sim2Real 部署全链路

```text
PyTorch checkpoint (.pt)
    ↓ torch.onnx.export()
ONNX 模型 (.onnx)
    ↓ onnx.checker.check_model()  ← 验证
    ↓ [MuJoCo Sim2Sim](./robot_modeling.md) 验证         ← 仿真验收，精度对比
    ↓
真机 NUC / Orin
    ↓ onnxruntime / TensorRT 推理
    ↓ humanoidController.cpp 加载 ONNX
    ↓ 50Hz 闭环推理 → 下发关节指令
```

### 关键踩坑

1. **`opset_version` 不兼容**：C++ 侧 ONNX Runtime 只支持特定 opset，版本不对直接加载失败
2. **输入维度不匹配**：C++ 侧 `humanoidController.cpp` 期望的 obs 维度必须和训练时**逐位对齐**，错一位就是垃圾输出
3. **观测归一化**：保存并加载训练时的统计量、裁剪规则和预处理顺序，或将预处理一并导出；必须保持训练与推理一致，不要求硬编码到 C++

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **ONNX** | 开放神经网络交换格式，跨框架的模型表示 |
| **TensorRT** | NVIDIA 推理优化引擎，图优化+层融合+量化 |
| **FP16** | 半精度浮点，实际速度和误差需在目标设备验证 |
| **INT8** | 8-bit 整数量化，量化参数与精度回归不可省略 |
| **opset** | ONNX 算子集版本号，决定 C++ Runtime 兼容性 |
| **Unified Memory** | Orin NX 架构特性：CPU 和 GPU 共享物理内存 |
