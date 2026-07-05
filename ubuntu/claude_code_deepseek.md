# Claude Code 配置与 DeepSeek 模型接入

> Claude Code 是 Anthropic 的 AI 编程助手 CLI，支持外接 OpenAI 兼容 API（如 DeepSeek）。本笔记记录在机器人开发环境中配置 Claude Code + DeepSeek 的实用命令与排障。

---

## 快速配置

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# DeepSeek（OpenAI 兼容端点）
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_API_KEY="sk-..."

# 或写入 ~/.bashrc / ~/.zshrc 持久化
claude
```

---

## 模型选择

| 场景 | 推荐模型 | 说明 |
|------|----------|------|
| 日常改代码 | `deepseek-chat` | 便宜、上下文长 |
| 复杂架构 | `deepseek-reasoner` | 推理链更长，适合读大仓库 |
| 文档整理 | `deepseek-chat` | 配合 `@文件` 引用笔记 |

在 Claude Code 内可用 `/model` 切换（若 API 支持）。

---

## 在机器人开发中的常用场景

- **跨文件重构**：修改行为树/VLA 管线时，一次性追踪所有依赖
- **架构咨询**：把思维导图/笔记扔给 Claude，问「这个架构还缺什么」
- **文档生成**：从代码注释自动生成 Markdown 笔记
- **终端排障**：直接粘贴 ROS / EtherCAT 报错日志，让 AI 分析根因
- **Diff 审查**：`git diff` 输出粘贴，检查是否破坏控制频率或 TF 链

---

## 与 Cursor 的分工

| 工具 | 适合 |
|------|------|
| **Cursor** | IDE 内补全、多文件编辑、Mermaid 预览 |
| **Claude Code** | 终端批量任务、脚本生成、无 GUI 的 SSH 环境 |

👉 详见 [Cursor 使用](./cursor.md) · [AI Coding Agent](./AI_Coding_Agent.md)

---

## 常见问题

| 问题 | 处理 |
|------|------|
| `401 Unauthorized` | 检查 `ANTHROPIC_API_KEY` 与 Base URL 是否匹配 DeepSeek 文档 |
| 响应截断 | 缩小单次 `@` 文件范围；分步提问 |
| 中文乱码 | 终端 `export LANG=zh_CN.UTF-8` |
| 代理环境 | 与 [auto_clash](./auto_clash.md) 一致设置 `HTTPS_PROXY` |

---

## 相关笔记

- [AI Coding Agent](./AI_Coding_Agent.md) — AI 编程助手对比
- [Cursor 使用](./cursor.md) — Cursor IDE 配置
- [AI 整理笔记](./AI_sort_out_notes.md) — 用 AI 归整碎片化记录
- [OpenClaw 本地 Agent](./openclaw.md) — 另一类本地自动化方案
