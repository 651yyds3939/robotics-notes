我已经将暂时关闭和禁用 Clash 服务的相关终端指令补充到了笔记的 **3.2 节**和 **第五部分 (SOP)** 中，其余内容和排版完全保持了原样。

你可以直接复制下面这份完整的笔记进行替换：

```markdown
---

# Ubuntu 开发环境代理调度与自动化配置完全手册

本手册涵盖从零部署 Clash 核心、配置系统全局代理、订阅链接转换，到进阶的多机场软链接调度、Systemd 开机自启及终端环境配置。

---

## 一、 初始化 Clash 运行环境与核心文件 (官方标准流程)

### 1. 获取 Clash 核心二进制文件

创建工作目录并下载官方提供的压缩包，解压后赋予执行权限。

```bash
mkdir ~/clash; cd ~/clash;
wget "[https://vk4fg.big-files.make-w0rld-static.club:8000/file/ikuuu-static-release/clash-linux/clash-linux-1.0.1/clash-linux-amd64.gz](https://vk4fg.big-files.make-w0rld-static.club:8000/file/ikuuu-static-release/clash-linux/clash-linux-1.0.1/clash-linux-amd64.gz)" -O clash-linux-amd64.gz;
gzip -d clash-linux-amd64.gz;
mv clash-linux-amd64 clash;
chmod +x clash;


```

### 2. 下载/准备配置文件 (config.yaml)

* **方案 A (终端直接下载)**：适用于机场直接提供 Clash 订阅链接的情况。

```bash
cd ~/clash
wget -O config.yaml "你的订阅链接"


```

* **方案 B (浏览器大法)**：若 wget 报错，直接在 Firefox 地址栏输入订阅 URL 回车下载，手动移动至 `~/clash/config.yaml`。

### 3. 本地启动测试

运行核心引擎以验证配置是否正确。

```bash
./clash -d .


```

*(注：看到监听 7890/9090 等端口的日志即为成功，按 `Ctrl+C` 退出)*

### 4. 面板管理 (Dashboard)

启动后可访问控制台进行节点切换：

* **访问地址**：`http://clash.razord.top/`
* **Host**：`127.0.0.1` | **端口**：`9090`

### 5. 配置 Ubuntu 系统全局代理

在 Ubuntu “设置” ➡️ “网络” ➡️ “网络代理” 中选择“手动”，填写：

* **HTTP/HTTPS**：`127.0.0.1` | 端口：`7890`
* **Socks 主机**：`127.0.0.1` | 端口：`7891`

---

## 二、 订阅转换与多机场模块化管理

### 2.1 非标准链接转换 (URL 转 YAML)

**方式一：终端指令直接获取**
务必加上 `--user-agent` 伪装成 Clash 客户端，否则有的机场会返回一堆乱码（Base64）。

```bash
wget --user-agent="clash-meta/v1.18.0" -O peiqian.yaml "你的机场订阅链接URL"

```

**方式二：使用转换器获取**
**场景**：若机场链接下载后是乱码或 Base64 文本，需通过转换器处理。

1. **打开转换器**：访问在线工具（如 `https://sub.v1.mk/`）。
2. **生成链接**：粘贴原始 URL，客户端选 **Clash**，点击“生成订阅链接”。
3. **下载文件**：在 Firefox 地址栏粘贴生成的链接并回车，下载得到的即为标准 `.yaml` 文件。

### 2.2 建立配置仓库

```bash
mkdir -p ~/clash/profiles


```

### 2.3 归档不同机场配置

将下载好的文件重命名并存入仓库。

```bash
# 举例：
mv ~/Downloads/下载的文件1.yaml ~/clash/profiles/flower.yaml
mv ~/Downloads/下载的文件2.yaml ~/clash/profiles/peiqian.yaml


```

### 2.4 软链接无缝切换 (核心技巧)

```bash
# 想要用哪个，就链接哪个。-s 创建链接，-f 强制覆盖。
ln -sf ~/clash/profiles/peiqian.yaml ~/clash/config.yaml
ln -sf ~/clash/profiles/huayun.yaml ~/clash/config.yaml
ln -sf ~/clash/profiles/iKuuu_V2.yaml ~/clash/config.yaml

#重启 Clash 守护进程
sudo systemctl restart clash

# 修正权限（可选，若出现小锁图标执行此条）
sudo chown -R $USER:$USER ~/clash


```

---

## 三、 自动化守护进程 (Systemd 开机自启)

实现开机静默运行、崩溃自动重启。

### 3.1 创建服务文件

```bash
sudo gedit /etc/systemd/system/clash.service


```

粘贴以下内容：

```ini
[Unit]
Description=Clash Daemon Service
After=network.target

[Service]
Type=simple
User=%i  # 替换为你的用户名
WorkingDirectory=~/clash
ExecStart=~/clash/clash -d .
Restart=on-failure

[Install]
WantedBy=multi-user.target


```

### 3.2 服务控制指令

```bash
sudo systemctl daemon-reload       # 重载配置
sudo systemctl enable clash        # 开机自启
sudo systemctl start clash         # 立即启动
sudo systemctl restart clash       # 修改/切换配置后执行重启
journalctl -u clash -f             # 实时查看运行日志
sudo systemctl stop clash          # 暂时关闭服务 (停止运行)
sudo systemctl disable clash       # 禁用开机自启


```

---

## 四、 终端局部代理 (针对 ROS2 / Github 开发)

解决终端 `git clone` 或 `apt` 不走代理的问题。

### 4.1 注入快捷开关

```bash
gedit ~/.bashrc


```

在末尾添加：

```bash
# 开启代理
alias proxy_on='export http_proxy=[http://127.0.0.1:7890](http://127.0.0.1:7890) https_proxy=[http://127.0.0.1:7890](http://127.0.0.1:7890) all_proxy=socks5://127.0.0.1:7890 && echo -e "Terminal Proxy: \033[32mON\033[0m"'

# 关闭代理
alias proxy_off='unset http_proxy https_proxy all_proxy && echo -e "Terminal Proxy: \033[31mOFF\033[0m"'


```

### 4.2 生效配置

```bash
source ~/.bashrc


```

---

## 五、 日常维护标准操作流 (SOP)

1. **更新订阅**：去浏览器回车下载新文件，移动并覆盖 `~/clash/profiles/` 下的对应文件。
2. **切换机场**：执行 `ln -sf ~/clash/profiles/目标机场.yaml ~/clash/config.yaml`。
3. **应用更改**：执行 `sudo systemctl restart clash`。
4. **暂时关闭代理**：执行 `sudo systemctl stop clash` 彻底关闭后台服务（若当前终端已开启代理，需配合执行 `proxy_off` 恢复直连）。

```

```