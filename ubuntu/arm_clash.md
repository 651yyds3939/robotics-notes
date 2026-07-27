# 🤖 机器人上位机全局代理 (Mihomo) 纯净部署指南
**适用环境**：NVIDIA Jetson Orin NX 等 ARM 架构设备 / Ubuntu 20.04**开发场景**：ROS 2 机器人（如双足人形 ROS 2 平台），需要外网拉取依赖且不能干扰本地局域网和 ROS 组播通信。
---

## 📌 核心思路在老版本的 Ubuntu 系统中，强行安装最新版图形化代理软件（如 Clash Verge）极易引发底层依赖冲突（`libwebkit2gtk` 等）。**最稳妥、零性能损耗的方案是：** `纯二进制内核 (Mihomo) 后台运行` + `Web 网页端可视化控制`。
---

## 🚀 部署步骤
### Step 1: 获取并升级 ARM64 最新内核（解决新协议不支持问题）*老版本内核无法识别 VLESS/Hysteria2 等新协议，会导致 `unsupported` 报错并闪退，必须升级到最新 ARM64 专属内核。*
1. 停止当前服务并下载最新内核：   ```bash
   sudo systemctl stop mihomo
   sudo wget -O /tmp/mihomo.gz [https://mirror.ghproxy.com/https://github.com/MetaCubeX/mihomo/releases/download/v1.18.4/mihomo-linux-arm64-v1.18.4.gz](https://mirror.ghproxy.com/https://github.com/MetaCubeX/mihomo/releases/download/v1.18.4/mihomo-linux-arm64-v1.18.4.gz)

```

2. 解压并赋予权限，替换旧核心：


```bash
sudo gzip -f -d /tmp/mihomo.gz
sudo chmod +x /tmp/mihomo
sudo mv /tmp/mihomo /usr/local/bin/mihomo

```



### Step 2: 获取纯净版节点文件（物理绕过网络报错）



*为防止终端 `wget` 下载时因无代理导致超时或出现 400 Bad Request 报错，直接使用浏览器下载。*

1. 在机器人 Ubuntu 桌面上，打开自带的 **Firefox 浏览器**。


2. 将**机场订阅链接**粘贴到地址栏，按回车。


3. 浏览器会自动下载一个包含节点的 `.yaml` 文件。


4. 将该文件重命名为 `nodes.yaml`，并将其移动到主目录（`~/`）下。



### Step 3: 注入机器人专属配置（防错修改法）



*为防止命令行 `cat <<EOF` 拼接造成的格式错乱，直接使用系统自带的记事本修改。*


*(强烈建议：使用你的笔记本电脑修改好配置文件，再用 U 盘拷贝至机器人的主目录，这样可以 100% 免疫 Linux 换行符陷阱！)*

1. 在主目录下双击打开刚才的 `nodes.yaml` 文件（默认会用 Text Editor 打开）。


2. **修改基础控制端口**：
在文件头部，确保包含以下设置（如果没有则手动加上，如果有则修改）：


```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: rule
log-level: info
external-controller: 0.0.0.0:9090
secret: ""

```


3. **添加 TUN 模式（接管系统全局流量）**：
找一个空行，粘贴以下配置：


```yaml
tun:
  enable: true
  stack: system
  auto-route: true
  auto-detect-interface: true

```


4. **添加 ROS 2 保护规则（防止机器人失联）**：
滑动到文件下方的 `rules:` 部分，在 `rules:` 下方的**第一行**插入以下直连规则（注意缩进空格）：


```yaml
  - IP-CIDR,224.0.0.0/4,DIRECT # ROS 2 组播通信必放行
  - IP-CIDR,192.168.0.0/16,DIRECT # 局域网 SSH 控制必放行
  - IP-CIDR,127.0.0.0/8,DIRECT # 本机回环必放行

```


5. 保存文件并关闭编辑器。



### Step 4: 补充核心数据库（打破内核启动假死循环）



*Mihomo 启动需要全球 IP 数据库 `Country.mmdb`。如果缺失，程序会陷入“尝试下载 -> 无代理卡死 -> 启动失败”的死循环。*

1. 在已配置梯子的笔记本电脑上，通过浏览器下载该文件：
[点击下载 Country.mmdb](https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb)


2. 通过 U盘 或 `scp` 命令将该文件传到机器人的主目录（`~/`）。


3. 在机器人终端执行，将其放入系统目录：


```bash
sudo mv ~/Country.mmdb /etc/mihomo/

```



### Step 5: 语法检查、备份与覆盖启动服务



*覆盖系统配置前，必须预先备份，并进行严格的语法检查！*

1. **测试配置文件语法**（确保手工添加的配置没有空格和缩进错误）：


```bash
sudo /usr/local/bin/mihomo -d /etc/mihomo -t

```


*(只有看到终端最后提示 `configuration test is successful` 才能继续下一步)*

2. **【重要】备份现有系统配置文件**：


```bash
sudo cp /etc/mihomo/config.yaml /etc/mihomo/config.yaml.bak

```


3. **覆盖配置并启动服务**：
配置和依赖均已就绪，在终端执行以下命令使代理生效：


```bash
# 将我们改好的完美配置文件覆盖到系统目录
sudo cp ~/nodes.yaml /etc/mihomo/config.yaml

# 重启 Mihomo 服务
sudo systemctl restart mihomo

```


4. **验证 9090 控制端口是否成功开放**：


```bash
curl [http://127.0.0.1:9090](http://127.0.0.1:9090)

```


> **成功标志**：只要终端返回 `{"hello":"mihomo"}`（或类似的 JSON 字符串），即说明底层代理已完美运行！
> 
> 



### Step 6: 连接可视化 Web 面板



后台已经跑通，最后只需用网页连接后台进行可视化控制：

1. 在机器人的浏览器中打开面板地址（注意必须是 `http`）：
👉 **http://clash.razord.top**


2. 在弹出的连接窗口中填写：


* **Host**: `127.0.0.1`

* **Port**: `9090`

* **Secret**: （保持为空）




3. 点击 **OK**。


4. 点击左侧 **Proxies (代理)**，选择目标节点。


5. 新开一个标签页，访问 `google.com` 或在终端执行代码拉取，享受全局流畅网络！



---

## 🧰 进阶配置与急救指南



### 进阶 1: 终端专属快捷翻墙命令



*尽管开启了 TUN 模式，但有时终端的 `git clone` 或 `apt` 等工具并不会主动走代理，建议配置 Bash 环境变量别名。*

1. 直接在终端输入以下命令写入 `~/.bashrc`：


```bash
echo -e "\nalias proxy='export http_proxy=[http://127.0.0.1:7890](http://127.0.0.1:7890);export https_proxy=[http://127.0.0.1:7890](http://127.0.0.1:7890);echo \"Proxy on\"'\nalias unproxy='unset http_proxy;unset https_proxy;echo \"Proxy off\"'" >> ~/.bashrc

```


2. 刷新配置使其立即生效：


```bash
source ~/.bashrc

```


3. **使用方法**：在需要拉取依赖前，输入 `proxy` 开启终端代理；使用完毕后输入 `unproxy` 关闭。你可以通过 `curl -I https://www.google.com` 来测试连通性。



### 进阶 2: 劫持死锁与断网急救（物理拔管法）



*如果遇到节点配置错误或内核崩溃导致 TUN 虚拟网卡发生死锁，系统路由和 DNS 会被强制劫持，造成国内网也无法连接。请按以下命令强行抢回控制权：*

1. 彻底封杀并禁用问题代理服务：


```bash
sudo systemctl stop mihomo
sudo systemctl disable mihomo

```


2. 强行重置 Ubuntu 网络管理器和 DNS 路由：


```bash
sudo systemctl restart NetworkManager
sudo systemctl restart systemd-resolved

```


3. 测试国内网络是否恢复：


```bash
ping baidu.com -c 4

```



*(如果在执行上述步骤后仍然断网，请直接祭出终极大招：在终端输入 `sudo reboot`。重启后，由于我们提前执行了 disable，代理不会自启，Ubuntu 会自动清空遗留的错误虚拟网卡和路由表，网络将彻底复原。)*

### 进阶 3: 安全停用代理并销毁配置（保留内核引擎）

*当你需要彻底关闭代理、清除个人账号与节点数据，但希望保留底层内核引擎以便日后随时复活时，请执行以下操作：*

1. **停止运行并禁用开机自启**：让代理内核彻底熄火，剥夺自启权限。
```bash
sudo systemctl stop mihomo
sudo systemctl disable mihomo

```


2. **销毁个人配置与残留文件**：删除系统目录中的代理配置和备份，并顺手清理主目录下的各类遗留文件，防止隐私泄露。
```bash
sudo rm -f /etc/mihomo/config.yaml
sudo rm -f /etc/mihomo/config.yaml.bak
rm -f ~/nodes.yaml ~/peiqian.yaml ~/old.yaml ~/config.yaml ~/final_config.yaml ~/tmp_nodes.yaml ~/robot_base.yaml

```


3. **重置网络管理器与 DNS**：防止 TUN 模式虚拟网卡残留导致网络死锁，确保彻底恢复纯净的国内直连网络。
```bash
sudo systemctl restart NetworkManager
sudo systemctl restart systemd-resolved

```
> **💡 未来复活指南**：日后需要再次翻墙时，只需按照 **Step 3** 准备好新的 `config.yaml` 并放入 `/etc/mihomo/` 系统目录下，然后执行 `sudo systemctl enable mihomo` 和 `sudo systemctl start mihomo` 即可一键满血复活！

