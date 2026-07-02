# Cursor AI IDE 环境配置与使用笔记

> 👉 相关：[具身智能工程工具箱](../robotics/tools.md) · [AI 编程 Agent](./AI_Coding_Agent.md) · [环境排障](../robotics/environment.md)

**Cursor 安装教程参考：** [CSDN 教程链接](https://blog.csdn.net/wangyx1234/article/details/149124333?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-9-149124333-blog-154054036.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.6&utm_relevant_index=12)

---

## 1. Cursor 与 VS Code 的核心区别
* **产品定位：** Cursor 并非 VS Code 的简单插件，而是一个独立且深度整合 AI 的全新 IDE（AI-native 进化版）。虽然 VS Code 依然是业界稳定性的标杆，但在复杂的工程开发中，Cursor 能带来显著的生产力提升。
* **核心优势：** 具备极其强大的**跨文件（Cross-file）代码分析与修改能力**，它能理解整个机器人项目工程的上下文逻辑，这远超常规的 AI 侧边栏插件。
* **兼容生态：** 完美兼容 VS Code 的底层生态，可以直接继承其海量的扩展插件（Extensions）和快捷键系统，迁移成本几乎为零。

## 2. Cursor 版本选择与体验差异
* **AppImage 与 .deb 版本的误区：** 在初次体验时，可能会感觉 `.deb` 安装版的功能或界面布局不如 `AppImage` 格式完善。但这其实主要是因为布局设置和默认配置的差异导致的错觉，两者在底层 AI 核心功能上并没有实质性的阉割。
* **推荐环境：** 在 Ubuntu 20.04/22.04 下，直接使用 `AppImage` 格式，配合终端快捷指令运行，是最干净、灵活且不污染系统的解决方案。

## 3. 如何同步 VS Code 配置到 Cursor
与 VS Code 同源，可将原有开发配置迁移如下：
* **内置引导提示：** 初次安装并打开 Cursor 时，启动界面会直接弹窗提供“一键导入 VS Code 扩展与设置”的引导。
* **命令面板同步：** 使用快捷键打开命令面板（`Ctrl + Shift + P`），搜索并选择 `Import Settings`（导入设置）相关选项进行同步。
* **手动硬核迁移：** 直接定位到原软件的配置目录，手动复制 `settings.json`（全局配置文件）和 `keybindings.json`（快捷键映射表）到 Cursor 的对应目录下，实现最精准的环境对齐。

## 4. Ubuntu 终端快捷启动配置 (解决核心痛点)
在 Linux 中直接运行 AppImage 需要输入长路径，且程序运行后会霸占终端并持续输出无用的后台日志。通过在 Zsh 配置文件中添加专属函数即可完美解决。

### ⚙️ 配置文件添加代码
执行 `nano ~/.zshrc`（或对应 shell 配置文件），在文件末尾添加：

```zsh
# Cursor 快速启动函数
cur() {
 /opt/cursor.appimage --no-sandbox "$@" > /dev/null 2>&1 &
}

```

*保存文件后，执行 `source ~/.zshrc` 使其立即生效。*

### 🧠 配置原理解析

* `/opt/cursor.appimage`：软件存放的绝对路径（需提前使用 `chmod +x` 赋予可执行权限）。
* `--no-sandbox`：解除 Ubuntu 沙盒限制。很多 AppImage 直接运行会因系统沙盒机制报错，添加此参数可确保稳定启动。
* `"$@"`：参数透传。可在命令行指定要挂载的当前目录 `.` 或具体文件，原封不动传给 IDE。
* `> /dev/null 2>&1`：日志黑洞。将程序的正常运行日志和报错信息全数丢弃，保持终端界面纯净。
* `&`：后台静默运行。将进程与当前终端剥离，敲下回车后终端立刻释放，随时可以输入下一条编译或运行指令。

## 5. 日常高效工作流体验

* **极速挂载当前项目：** 在终端进入目标代码工程，直接输入 `cur .`，Cursor 会瞬间在后台启动并自动加载当前文件夹上下文。
* **单文件精准编辑：** 遇到需要快速修改的系统文件，输入 `cur ~/.config/starship.toml`，即可跨过繁琐的 GUI 菜单，直达代码。


# Ubuntu 20.04 解决 Cursor 设备锁（Too Many Free Trials）与 AI 助手注入全记录

本篇文档记录了在 Ubuntu 20.04 环境下，针对原本在 `/opt` 目录下以 `AppImage` 格式运行的 Cursor，解决“Too many free trials”设备锁限制，并彻底打通第三方“AI 助手”一键无感换号工具的完整排查与修复步骤。

---

## 核心问题分析

1. **“Too many free trials” 机制**：Cursor 会通过读取本地 `~/.config/Cursor/User/globalStorage/storage.json` 配置文件中的机器标识符（如 `telemetry.machineId` 等）来锁定设备。
2. **网络环境受限**：由于国内无法直接连接 GitHub 的 `raw.githubusercontent.com`，导致网传的开源一键重置脚本（`curl | bash`）直接报 443 错误。
3. **AppImage 格式与助手冲突**：第三方 AI 助手软件的原理是向 Cursor 的主程序核心（如 `resources/app`）注入劫持脚本。而 `.AppImage` 是只读的单文件镜像，且解压后的核心藏在深层的 `usr/share/cursor` 目录下，导致助手深度检测一直报 “未找到 Cursor 安装” 或 “未找到 workbench 文件”。
4. **Linux 权限拦截陷阱**：在使用 `sudo` 权限将解压文件移入系统目录后，文件所有者变成了 `root`。由于 AI 助手是以普通用户权限运行的，导致其虽然显示“已注入”，但实际无权修改底层特征，造成“虽然换了号，但底层设备 ID 没变，依然弹窗提示设备被锁”。

---

## 最终闭环解决方案（四步通关法）

请严格按照以下步骤操作，即可彻底解决设备锁并完美对接 AI 助手。

### 第一步：将 AppImage 转换为标准 Linux 安装版

我们需要将只读的单文件解压，并放置到 Linux 的官方标准路径下，以满足 AI 助手的深度检测逻辑。

打开终端，直接复制并运行以下整段命令（已隐去注释防止终端报错）：

```bash
cd /opt
sudo ./cursor.appimage --appimage-extract
sudo mkdir -p /usr/share/cursor
sudo cp -r squashfs-root/usr/share/cursor/* /usr/share/cursor/
sudo rm -rf squashfs-root
sudo ln -sf /usr/share/cursor/cursor /usr/bin/cursor

```

### 第二步：彻底释放文件权限（核心关键）

使用 `sudo` 解压后，须将目录所有权改回当前用户，否则辅助工具可能无法写入配置。

在终端运行以下命令：

```bash
sudo chown -R $USER:$USER /usr/share/cursor

```

### 第三步：在 AI 助手内重新执行注入与换号

此时管道和权限已经全部彻底打通，请在辅助软件中完成逻辑闭环：

1. **完全关闭** Cursor。
2. 打开 **AI 助手** 界面，此时最上方应该会自动识别并显示绿色的 **`● 已安装`**（`✓ 已找到 /usr/bin`）。
3. 如果下方的注入状态是灰色的，请点击右侧紫色的 **「注入 Cursor」** 按钮，确保其变为绿色的 **`● 已注入`**。
*(如果之前注入过，建议先点一次「还原 Cursor」再点「注入 Cursor」以确保补丁在正确权限下写入)*。
4. 点击中间蓝色的 **「获取账号并登录」** 按钮。
* **此时观察：** 软件界面上的当前账号应当被成功刷新为一个全新的陌生邮箱。在第二步释放权限后，这个动作会真正把底部的旧设备 ID 抹除，生成全新的虚拟硬件特征。



### 第四步：从助手内拉起 Cursor

1. 点击助手右上角的紫色 **「启动」** 按钮（或直接从系统打开 Cursor）。
2. 此时，全新的设备 ID + 全新的账号双重生效，右下角的“Too many free trials”弹窗将彻底消失！

---

## 备用方案：抛弃助手，纯本地手工强制解锁

如果未来因为辅助软件自身 Bug 导致换号失败，或者不想再依赖此类软件，可以使用以下纯手工方法一键强制重置设备锁。

1. **完全关闭 Cursor**：
```bash
pkill -f "Cursor"

```



```

2. **在终端执行本地 Python 脚本（利用 UUID 强制随机生成全套新机器特征）**：
 ```bash
 python3 -c "
 import json, os, uuid
 path = os.path.expanduser('~/.config/Cursor/User/globalStorage/storage.json')
 os.makedirs(os.path.dirname(path), exist_ok=True)
 try:
 with open(path, 'r') as f: data = json.load(f)
 except:
 data = {}
 data['telemetry.machineId'] = uuid.uuid4().hex
 data['telemetry.macMachineId'] = uuid.uuid4().hex
 data['telemetry.devDeviceId'] = str(uuid.uuid4())
 data['telemetry.sqmId'] = '{' + str(uuid.uuid4()).upper() + '}'
 for k in list(data.keys()):
 if 'auth' in k.lower() or 'token' in k.lower(): del data[k]
 with open(path, 'w') as f: json.dump(data, f, indent=2)
 print('🎉 本地硬件标识符强制重置成功！')
 "

```

3. **【关键防护】将配置文件锁死为只读，阻止官方检测回写**：
```bash
chmod 444 ~/.config/Cursor/User/globalStorage/storage.json

```



```

4. **阻止其自动下载更新补丁**：
 ```bash
 rm -rf ~/.config/cursor-updater
 touch ~/.config/cursor-updater
 chmod 444 ~/.config/cursor-updater

```

5. **换号登录**：手动打开浏览器使用无痕模式（`Ctrl + Shift + N`）在 Cursor 官网注册一个新邮箱账号，并在 Cursor 内登录该新账号即可。

---

### 常见疑问与避坑指南

* **本地聊天记录会丢吗？**
不会。Cursor 基于 VS Code，项目和本地的 Chat/Composer 聊天记录保存在项目专属的 `workspaceStorage` 中，重置设备 ID 和删除缓存不会影响代码和本地工作区历史。
* **为什么一定要用浏览器无痕模式注册？**
如果不用无痕模式，浏览器本地残留的 Cookie 会让 Cursor 官网可能识别为同一设备。新账号在注册的瞬间就会在云端被标记成同一台设备，导致一登录就再次弹窗。
* **切记：** 使用 AI 助手期间，**绝对不要**在 Cursor 软件内部点击 `Log out` 退出登录，一切换号操作均在助手面板点击「获取账号并登录」完成。