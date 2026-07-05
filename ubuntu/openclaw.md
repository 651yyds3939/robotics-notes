
---

# 🦞 OpenClaw (龙虾) Ubuntu 部署与硬核调教全记录

这份“龙虾”（OpenClaw）的从零到一折腾史绝对值得记录下来。这不仅是一份部署文档，更是咱们真金白银踩过无数坑后总结出的避坑圣经。

为你整理了一份结构化的完整文档，建议直接保存为 Markdown 格式，方便随时查阅。

## 一、 基础环境配置与 OpenClaw 安装

OpenClaw 底层依赖 Node.js 运行环境。为了避免系统权限和版本冲突，最稳妥的方式是使用 NVM (Node Version Manager) 来管理环境。

**1. 安装 NVM 与 Node.js**
在终端中依次执行：

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 刷新环境变量（根据你的环境，刷新 zshrc）
source ~/.zshrc

# 安装 Node.js (OpenClaw 需要 Node 22 LTS 或 24 版本)
nvm install 24
nvm use 24
```

**2. 全局安装 OpenClaw**
通过 npm 直接全局安装龙虾的核心包：

```bash
npm install -g openclaw
```

**3. 验证安装**

```bash
openclaw --version
```

*(只要正常输出版本号，说明地基已经打好，可以进入后续的部署阶段。)*

---

## 二、 Ubuntu 纯净部署全流程

经历过底层的状态机崩溃后，最稳妥的部署方式永远是“终端命令行驱动”。

**1. 摧毁旧环境（如需重置）**
确保后台没有任何僵尸进程，并彻底清空损坏的配置：

```bash
systemctl --user stop openclaw-gateway
rm -rf ~/.openclaw
```

**2. 启动初始化向导**
运行官方引导命令，全程在终端内完成初始框架搭建：

```bash
openclaw onboard
```

**向导极速通关选项：**

* **设置模式：** 选择 `QuickStart（推荐）`。
* **模型/认证：** 先随意选择一个默认的（如 OpenAI 及其 Key），或者直接跳过，因为后续我们会用更强大的命令覆盖。
* **其他功能配置：** （搜索、技能、频道等）一路全部选择 **`暂时跳过`** 或 **`No`**。
* **启动方式：** 选择 **`在终端中启动`** 或 **`稍后启动`**。

**3. 配置核心大模型（以 DeepSeek 为例）**
**核心原则：永远使用终端配置模型，远离网页端配置框。**

```bash
openclaw configure
```

* 选择 **`Model`** -> 选择你要接入的模型（如 **`DeepSeek`**）。
* 系统会自动拉取并安装 npm 原生插件包（如 `@openclaw/deepseek-provider`）。
* 填入对应的 API Key。

**4. 启动与访问**
配置完成后，重启网关服务并打开控制面板：

```bash
systemctl --user restart openclaw-gateway
openclaw dashboard
```

浏览器会自动弹出一个带有全新安全 Token 的页面，点击 **`+ 新会话`** 即可开始交流。

---

## 三、 踩坑复盘：为什么一开始频频死机？

在早期的配置中，我们反复遭遇了阴魂不散的 `GatewayRequestError: unknown parent session: agent:main:main` 报错，导致网页无法连接。

### 🚨 失败的根本原因

* **网页 UI 的隐性 Bug：** OpenClaw 的前端自定义配置表单在生成 JSON 文件时，容易遗漏底层系统级字段，生成畸形的配置数据。
* **JSON Schema 校验极度严苛：** 我们试图在系统自带的 OpenAI 通道中，强行挂载一个非官方中转站 URL，并塞入一个系统名录里根本不存在的模型名（`gpt-5.5`）。
* **代理智能体（Agent）脑死亡：** 底层网关在启动 `main` 智能体时，发现它绑定的 `gpt-5.5` 模型在官方支持库里找不到。智能体初始化直接崩溃，导致前端永远找不到合法的父级会话（Parent Session）。

### 🛠️ 最终的破局之道

* **放弃打补丁，直接核弹重置：** 遇到底层状态机乱套，手动 `rm -rf sessions` 往往会破坏文件树。必须直接删除整个 `~/.openclaw` 文件夹重新初始化。
* **降维打击，回归终端：** 放弃网页端配置，使用 `openclaw configure`。这个命令不仅是填参数，它会在底层自动触发 `npm install` 拉取官方适配的 Provider 插件（例如 DeepSeek 的原生支持包）。依赖齐整，环境干净，瞬间满血复活。

---

## 四、 “龙虾”的完全体能力展示

OpenClaw 并非一个简单的聊天套壳，它是一个可以长出“手脚”和“嘴巴”的 AI 智能体网关（Agent Gateway）。

**1. 技能与工具链扩展 (Skills)**
通过 `openclaw configure -> Skills`，可以让它突破文本的限制：

* 在线搜索最新技术文档和资料。
* 读写本地系统文件。
* 接入 Trello、GitHub 等效率工具管理任务。

**2. 全渠道分身 (Channels)**
通过 `openclaw configure -> Channels`，可以把它部署到任何沟通平台：

* 接入飞书 (Feishu)，成为团队技术支持机器人。
* 接入 Telegram 或 Discord，随时随地在手机上向它下达指令。

**3. 模型无缝热切换 (Providers)**
通过终端安装不同的插件包，可以在控制台无缝切换 Claude 3.5、GPT-4o、DeepSeek 等各类顶级模型，根据不同任务分配不同的大脑。

---

## 五、 机器人研发专属副驾驶场景

在 C++ 开发和硬件调试的高强度节奏中，“龙虾”可以深度嵌入到开发流中，解决具体的工程问题。

**1. 运动控制逻辑调试**
当你用 C++ 编写底层运动控制代码时，它能快速帮你梳理逻辑死结。例如在物理机器人上部署“打太极”这类复杂的连续运动控制案例时，它可以协助优化算法时序，并且完全契合任务驱动、实践优先的编程学习风格，直接从你抛出的具体报错日志中给出修改方案。

**2. 硬件建模与仿真排错**
无论是调试 Fishbot 还是 Kuavo 平台，编写和修改 URDF 配置文件往往繁琐且容易漏掉坐标系转换细节。它可以迅速检查 URDF 树状结构，修正 Joint 和 Link 的惯性张量、碰撞系参数，大幅减少在 RViz 或 Gazebo 中因为模型错误导致的崩溃时间。

**3. 硬件选型与算力对比**
在评估运行视觉算法或 SLAM 的上位机时，它可以迅速拉取并对比最新设备（如联想拯救者系列、各类带有特定 GPU 的开发板）的详细算力规格，辅助你做出最佳的硬件采购和架构决策。

**4. 自动化文档与工作流**
开发过程中的大量零散代码片段、控制台输出日志，都可以直接扔给它。它能够极速将这些碎片信息排版成结构极其清晰的 Markdown 笔记。在需要向徐老师提交项目进度报告时，它可以帮你把干涩的代码逻辑转化为专业、有条理的技术汇报。

**5. 语言环境与前沿追踪**
面对即将到来的格拉斯哥大学研究生学业以及前期的语言班，它可以作为高强度的英语陪练。你可以把海外最新的机器人顶级会议论文（如 ICRA、IROS）的 PDF 丢给它，让它迅速提炼核心算法创新点，打破语言壁垒。

---

## 六、 常用保命命令备忘录

为了防止未来再次陷入僵局，请将以下命令刻在 DNA 里：

| 操作目的 | 终端命令 |
| --- | --- |
| **一键启动控制面板** | `openclaw dashboard` |
| **添加/修改模型与插件** | `openclaw configure` |
| **重启底层网关服务** | `systemctl --user restart openclaw-gateway` |
| **查看服务运行状态** | `systemctl --user status openclaw-gateway` |
| **强制注入中转站 URL** | `openclaw config set models.providers.openai.baseUrl "你的URL"` |
| **获取当前网关安全 Token** | `openclaw config get gateway.auth.token` |
| **核弹级重置（慎用）** | `systemctl --user stop openclaw-gateway && rm -rf ~/.openclaw` |