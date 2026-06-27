# Ubuntu/ROS 软件源与 GPG 密钥修复排坑笔记

## 1. 核心报错现象
在 Ubuntu 20.04 执行 `sudo apt update` 时，出现以下连环报错：
1. **公钥缺失**：`NO_PUBKEY F42ED6FBAB17C654` (ROS 官方源签名验证失败)。
2. **无效数据包**：`invalid packet (ctb=3c)` 和 `unsupported filetype` (尝试下载密钥后出现的新报错)。

## 2. 深度病理分析 (为什么常规方法没用？)

* **传统方法失效**：Ubuntu 20.04 及更高版本逐渐废弃了 `apt-key adv` 这类老方法。即使系统提示“密钥已存在(未改变)”，APT 更新时依然可能报错，因为密钥没有被存放在真正被信任的 `/etc/apt/trusted.gpg.d/` 文件夹中。
* **源冲突与累赘**：系统中同时存在三个 ROS 源（官方源、清华源、中科大源）。国内源已连通，但官方源（`packages.ros.org`）不仅网络极慢，且极其挑剔，是引发 `NO_PUBKEY` 的罪魁祸首。
* **致命的 `ctb=3c` 报错真相**：
  * 在尝试通过 `curl` 或 `wget` 结合镜像（如 ghproxy、中科大镜像）强制下载 `ros.key` 文件时，如果遇到网络阻断或文件不存在，镜像站会返回一个 **HTML 报错网页**（比如 `404 Not Found`）。
  * 终端强行把这个 HTML 网页当成密钥保存进了 `trusted.gpg.d`。
  * `3c` 是 `<`（HTML 标签开头）的十六进制码。这就导致 APT 在读取密钥时直接“中毒”，引发满屏的 `unsupported filetype` 警告。

---

## 3. 终极暴力修复方案 (纯本地，零网络依赖)

既然网络下载的密钥文件不靠谱，且真正的密钥其实早就在系统旧数据库里了，我们可以直接采用“本地提取 + 清理冗余”的方案解决。

### 第一步：排毒 (清理坏掉的伪装文件)
删除由于下载失败导致的带有 HTML 网页内容的假密钥文件，消除 `unsupported filetype` 警告：
```bash
sudo rm /etc/apt/trusted.gpg.d/ros-archive-keyring.gpg

```

### 第二步：借位 (从本地旧钥匙串导出并转换格式)

利用系统曾经缓存过的密钥记录，将其导出并用 `gpg --dearmour` 转换为 APT 真正认可的新格式，直接塞进目标文件夹。**此过程完全不需要联网**：

```bash
sudo apt-key export F42ED6FBAB17C654 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/ros-archive-keyring.gpg

```

*(注：如果终端弹出 `Warning: apt-key output should not be parsed...` 属于正常现象，忽略即可。)*

### 第三步：斩草除根 (干掉卡脖子的官方源)

既然清华源（TUNA）和中科大源（USTC）已经完美命中，完全没有必要保留极其卡顿的官方源。直接将其删除，加速后续更新：

```bash
sudo rm /etc/apt/sources.list.d/ros-latest.list

```

### 第四步：最终验证

重新执行更新命令：

```bash
sudo apt update

```

**结果**：所有报错消失，终端全部显示绿色的“命中”或“获取”，软件源经脉彻底打通。

