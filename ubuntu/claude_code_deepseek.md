# 🚀 Claude Code 接入 DeepSeek 官方完全指南

本指南将详细介绍如何通过修改环境变量，将 Anthropic 官方的 **Claude Code**（包含 VS Code/Cursor 插件及终端 CLI 工具）后端无缝替换为 **DeepSeek 官方 API**。通过本配置，你可以在完整保留 Claude Code 原生智能体（Agent）工作流的同时，享受到国内物理直连的低延迟以及超高性价比。

---

## 📋 准备工作

1. **获取 DeepSeek API Key**：
登录 **[platform.deepseek.com](https://platform.deepseek.com)** 官方控制台，进入 `API keys` 页面生成一个新的密钥。**(请务必妥善保管，切勿上传至公开仓库)**。
2. **确认账户余额**：
确保账户中有充足的可用额度（建议充值最低限额，防止高频自动化扫描触发欠费停机）。

---

## 🛠️ 方案一：IDE 篇（VS Code / Cursor 插件接入）

如果你主要通过 VS Code 或 Cursor 的右侧面板、侧边栏聊天框或者行内补全使用 Claude Code，你有两种级别的地方可以配置。

在配置前，请先根据需求选择以下两款官方标准的 **DeepSeek-V4 环境变量模板** 之一：

> ### 💡 模板 A：超低成本·极致续航（全面采用 Flash 模型）
> 
> 
> 适合高频编码、大面积项目空间自动化扫描调试。此配置单次请求费用极低，能有效防止钱包意外熔断。
> ```json
> "claudeCode.environmentVariables": [
>     { "name": "ANTHROPIC_BASE_URL", "value": "https://api.deepseek.com/anthropic" },
>     { "name": "ANTHROPIC_AUTH_TOKEN", "value": "你的_DEEPSEEK_API_KEY" },
>     { "name": "ANTHROPIC_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "ANTHROPIC_DEFAULT_OPUS_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "ANTHROPIC_DEFAULT_SONNET_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "CLAUDE_CODE_SUBAGENT_MODEL", "value": "deepseek-v4-flash" }
> ]
> 
> ```
> 
> 
> ### 🧠 模板 B：硬核推理·全功能（全面采用 Pro[1m] 顶配模型）
> 
> 
> 适合需要长上下文理解、极高难度算法重构的深度攻坚场景。**注意：`[1m]` 代表启用 100 万超大上下文窗口；`SUBAGENT` 保留为 flash 帮主脑干杂活，效率最高。**
> ```json
> "claudeCode.environmentVariables": [
>     { "name": "ANTHROPIC_BASE_URL", "value": "https://api.deepseek.com/anthropic" },
>     { "name": "ANTHROPIC_AUTH_TOKEN", "value": "你的_DEEPSEEK_API_KEY" },
>     { "name": "ANTHROPIC_MODEL", "value": "deepseek-v4-pro[1m]" },
>     { "name": "ANTHROPIC_DEFAULT_OPUS_MODEL", "value": "deepseek-v4-pro[1m]" },
>     { "name": "ANTHROPIC_DEFAULT_SONNET_MODEL", "value": "deepseek-v4-pro[1m]" },
>     { "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "CLAUDE_CODE_SUBAGENT_MODEL", "value": "deepseek-v4-flash" },
>     { "name": "CLAUDE_CODE_EFFORT_LEVEL", "value": "max" }
> ]
> 
> ```
> 
> 

选好模板后，选择以下**途径 1** 或**途径 2** 填入编辑器：

### 途径 1：配置为“全局大总管”（对所有项目永久生效）

1. 按下快捷键 **`Ctrl + Shift + P`**，输入 **`Preferences: Open User Settings (JSON)`** 并回车，进入全局用户配置。
2. 将选好的模板代码直接粘贴进 JSON 的根大括号 `{}` 内部即可。
* *注：Linux 下该文件实际路径为 `~/.config/Code/User/settings.json`（Cursor 为 `~/.config/Cursor/User/settings.json`）。*



### 途径 2：配置为“项目小专属”（仅对当前打开的文件夹生效）

1. 在你当前打开的机器人工程根目录下，检查或新建一个名为 **`.vscode`** 的文件夹。
2. 在该文件夹下新建一个 **`settings.json`** 文件（即项目的局部配置文件，Cursor 同样完美兼容此路径）。
3. 用大括号包裹你的模板并保存。例如：
```json
{
    "claudeCode.environmentVariables": [
        { "name": "ANTHROPIC_BASE_URL", "value": "https://api.deepseek.com/anthropic" },
        ...
    ]
}

```



*配置完成后，务必按 `Ctrl + Shift + P` 执行 `Developer: Reload Window` 重载窗口使其生效。*

---

## 💻 方案二：终端篇（CLI 命令行工具永久接入）

如果你习惯直接在 Linux/Mac 终端里切换到代码目录，然后敲击 `claude` 命令启动 Agent 肉搏，请使用以下方式：

### 方式 A：修改 CLI 专属全局配置文件（最推荐，永久生效）

由于终端 `claude` 命令是独立于编辑器的程序，它有自己的中央配置文件：

1. 打开或创建全局 CLI 配置文件：
* **Linux / macOS**: `~/.claude/settings.json`
* **Windows**: `C:\Users\<你的用户名>\.claude\settings.json`


2. 将对应的环境配置写入该文件（以 Pro 顶配版为例）：
```json
{
    "env": {
        "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "你的_DEEPSEEK_API_KEY",
        "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
        "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
        "CLAUDE_CODE_EFFORT_LEVEL": "max"
    }
}

```



### 方式 B：当前终端临时单次生效（命令行注入）

如果你只是临时测试，可以直接在终端运行命令（会话关闭后失效）：

* **Linux / macOS (自由切换 Bash/Zsh)**:
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=你的_DEEPSEEK_API_KEY
export ANTHROPIC_MODEL=deepseek-v4-flash
claude

```



---

## 🎛️ 验证连接状态

无论是用插件还是终端工具，接入成功后，在 Claude Code 的聊天对话框中直接输入内置诊断命令：

```bash
/status

```

> **🎯 预期正常返回结果：**
> * **Base URL**: 显示为 `[https://api.deepseek.com/anthropic](https://api.deepseek.com/anthropic)`
> * **Model**: 显示为你刚才配置对应的 `deepseek-v4-*`
> * 能够正常读取当前工作目录并执行只读命令（如 `ls` ）。
> 
> 

---

## ⚠️ 避坑与高级调优指南

### 1. 代理软件（VPN/Clash）冲突减速

由于 DeepSeek 的官方服务器完全部署在国内骨干网，**请求不需要翻墙**。

* **潜在隐患**：如果你的系统挂着代理软件的 **全局模式（Global）**，数据会绕到海外节点再返回，导致延迟暴增、丢包或异常报错。
* **调优建议**：确保将代理软件切换为 **规则模式（Rule）**，或手动将 `deepseek.com` 加入**直连（Direct）白名单**，确保物理直连红利最大化。

### 2. 多线程自动化编译防护（如 ROS 开发、C++ 大型项目）

当 Claude Code 作为智能体在后台运行并帮你解决编译问题时，它可能会自主调用底层的编译器（如 `catkin`、`make`、`cmake`）。

* **内存风暴**：C++ 编译器在多核心并发时极其消耗系统内存（RAM）。如果你的机器属于轻量级嵌入式主板或只有 8G 内存，全核满载编译极易导致系统崩溃。
* **防护方案**：建议在涉及编译交互前，提前在环境中显式限制编译线程（例如手动在终端执行 `catkin_make -j2` 或 `make -j2`），避免智能体无脑拉满多核撑爆本地系统虚拟内存（Swap）。

### 3. 多模态视觉限制说明

* `deepseek-v4` 的主线工程 API 目前专注于纯代码、长上下文逻辑和极高并发的高性价比推理。这意味着将任何 **图片（UI截图、设计草图、Rviz可视化点云截图）** 直接拖入由该 API 驱动的 Claude Code 窗口时，会引发通道不匹配的报错。
* **最佳方案**：若需要看图改代码或分析 UI 截图，请切换到支持原生多模态视觉的独立软件（如免费额度内的 Cursor 视觉组件或 Claude 官方网页版），完成“视觉到文本描述”的转换后，再将文字交给 DeepSeek 接口处理。