# Claude Code 配置与 DeepSeek 模型接入

> Claude Code 是 Anthropic 的 AI 编程助手 CLI，支持外接第三方模型（如 DeepSeek）。本笔记记录在机器人开发环境中配置 Claude Code + DeepSeek 的实用命令。

---

## 快速配置

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 配置第三方模型（DeepSeek）
export ANTHROPIC_BASE_URL="https://api.deepseek.com"
export ANTHROPIC_API_KEY="sk-..."

# 启动
claude
```

---

## 在机器人开发中的常用场景

- **跨文件重构**：修改行为树/VLA 管线时，一次性追踪所有依赖
- **架构咨询**：把思维导图/笔记扔给 Claude，问"这个架构还缺什么"
- **文档生成**：从代码注释自动生成 Markdown 笔记
- **终端排障**：直接粘贴报错日志，让 AI 分析根因

---

## 相关笔记

- [AI Coding Agent](./AI_Coding_Agent.md) — AI 编程助手对比
- [Cursor 使用](./cursor.md) — Cursor IDE 配置
- [AI 整理笔记](./AI_sort_out_notes.md) — 用 AI 归整碎片化记录
