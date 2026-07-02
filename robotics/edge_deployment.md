# 边缘端模型部署 —— ONNX / TensorRT 实战

> **核心定位**：PyTorch 训练的模型不能直接在机器人上跑——它又大又慢。边缘部署的核心任务是把训好的策略网络**导出、优化、塞进机器人的板载算力中**，在毫秒级延迟内完成推理。
>
> 👉 实战笔记：[RL Sim2Real ONNX 部署](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md)

---

## 第 0 章：边缘部署一句话

> **大白话**：GPU 上训练得到的 [RL 策略](./RL.md) 常为数百 MB 的 PyTorch checkpoint。机载 NUC/Orin 无桌面级 GPU，需将策略压缩为 ONNX/TensorRT），能在 1ms 内出结果。

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

# 验证 ONNX 模型结构完整性
model = onnx.load("kuavo_policy.onnx")
onnx.checker.check_model(model)

# 对比推理精度：ONNX vs PyTorch 针对同一输入
ort_session = onnxruntime.InferenceSession("kuavo_policy.onnx")
onnx_output = ort_session.run(None, {"observations": dummy_input.numpy()})
torch_output = policy(dummy_input).detach().numpy()

assert np.allclose(onnx_output, torch_output, atol=1e-5), "精度不匹配！"
```

---

## 第 2 章：TensorRT —— NVIDIA 的推理加速器

TensorRT 是 NVIDIA 的推理优化引擎，对 ONNX 模型做图优化、层融合、精度量化。

| 优化方式 | 原理 | 推理速度提升 | 精度损失 |
|----------|------|------------|---------|
| **FP16** | 半精度浮点 | 1.5-2× | 微小，通常可忽略 |
| **INT8** | 8-bit 整数量化 | 3-4× | 需要校准集，有风险 |
| **Layer Fusion** | 合并相邻算子（Conv+BatchNorm+ReLU） | 10-30% | 无损 |

### 2.1 导出 TensorRT Engine

```bash
# 命令行导出（推荐，自动处理版本兼容）
trtexec --onnx=kuavo_policy.onnx \
 --saveEngine=kuavo_policy.trt \
 --fp16 \
 --workspace=2048
```

### 2.2 Orin NX 部署注意

- Orin NX 的 GPU 显存和 CPU 内存**物理共享**（Unified Memory），模型不能太大
- FP16 是 Orin 上性价比最高的选择——精度损失微乎其微，推理速度翻倍
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
3. **观测归一化**：训练时做的 normalization（均值/方差）必须**硬编码**到 C++ 推理管线中，不能丢

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **ONNX** | 开放神经网络交换格式，跨框架的模型表示 |
| **TensorRT** | NVIDIA 推理优化引擎，图优化+层融合+量化 |
| **FP16** | 半精度浮点，推理速度翻倍，精度损失小 |
| **INT8** | 8-bit 整数量化，最大速度但需校准集 |
| **opset** | ONNX 算子集版本号，决定 C++ Runtime 兼容性 |
| **Unified Memory** | Orin NX 架构特性：CPU 和 GPU 共享物理内存 |
