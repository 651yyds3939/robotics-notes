
# 🤖 机器人上位机全局代理 (Mihomo) 纯净部署指南

**适用环境**：NVIDIA Jetson Orin NX 等 ARM 架构设备 / Ubuntu 20.04
**开发场景**：ROS 2 机器人（如夸父 Kuavo），需要外网拉取依赖且不能干扰本地局域网和 ROS 组播通信。

---

## 📌 核心思路
在老版本的 Ubuntu 系统中，强行安装最新版图形化代理软件（如 Clash Verge）极易引发底层依赖冲突（`libwebkit2gtk` 等）。
**最稳妥、零性能损耗的方案是：** `纯二进制内核 (Mihomo) 后台运行` + `Web 网页端可视化控制`。

---

## 🚀 部署步骤

### Step 1: 获取纯净版节点文件（物理绕过网络报错）
*为防止终端 `wget` 下载时因无代理导致超时或出现 400 Bad Request 报错，直接使用浏览器下载。*

1. 在机器人 Ubuntu 桌面上，打开自带的 **Firefox 浏览器**。
2. 将你的**机场订阅链接**粘贴到地址栏，按回车。
3. 浏览器会自动下载一个包含节点的 `.yaml` 文件。
4. 将该文件重命名为 `nodes.yaml`，并将其移动到你的**主目录（Home, 即 `~/`）**下。

### Step 2: 注入机器人专属配置（图形化编辑防错）
*为防止命令行 `cat <<EOF` 拼接造成的格式错乱，直接使用系统自带的记事本修改。*

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
  - IP-CIDR,224.0.0.0/4,DIRECT      # ROS 2 组播通信必放行
  - IP-CIDR,192.168.0.0/16,DIRECT   # 局域网 SSH 控制必放行
  - IP-CIDR,127.0.0.0/8,DIRECT      # 本机回环必放行

```


5. 保存文件并关闭编辑器。

### Step 3: 补充核心数据库（打破内核启动假死循环）

*Mihomo 启动需要全球 IP 数据库 `Country.mmdb`。如果缺失，程序会陷入“尝试下载 -> 无代理卡死 -> 启动失败”的死循环。*

1. 在你的笔记本电脑（已挂梯子）上，通过浏览器下载该文件：
[点击下载 Country.mmdb](https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb)
2. 通过 U盘 或 `scp` 命令将该文件传到机器人的主目录（`~/`）。
3. 在机器人终端执行，将其放入系统目录：
```bash
sudo mv ~/Country.mmdb /etc/mihomo/

```



### Step 4: 覆盖配置并启动服务

配置和依赖均已就绪，在终端执行以下命令使代理生效：

```bash
# 1. 将我们改好的完美配置文件覆盖到系统目录
sudo cp ~/nodes.yaml /etc/mihomo/config.yaml

# 2. 重启 Mihomo 服务
sudo systemctl restart mihomo

# 3. 验证 9090 控制端口是否成功开放
curl [http://127.0.0.1:9090](http://127.0.0.1:9090)

```

> **成功标志**：只要终端返回 `{"hello":"mihomo"}`（或类似的 JSON 字符串），即说明底层代理已完美运行！

### Step 5: 连接可视化 Web 面板

后台已经跑通，最后只需用网页连接后台进行可视化控制：

1. 在机器人的浏览器中打开面板地址（注意必须是 `http`）：
👉 **http://clash.razord.top**
2. 在弹出的连接窗口中填写：
* **Host**: `127.0.0.1`
* **Port**: `9090`
* **Secret**: （保持为空）


3. 点击 **OK**。
4. 点击左侧的 **Proxies (代理)**，选择你需要使用的节点。
5. 新开一个标签页，访问 `google.com` 或在终端执行代码拉取，享受全局流畅网络！

```

```