# 📦 Docker 容器化与系统欺骗高级指南

> **核心摘要**：Docker 不是虚拟机（Virtual Machine），它是利用 Linux 内核特性实现的**进程隔离**。理解它，是进入企业级机器人开发的第一道门槛。本笔记涵盖了容器挂载逻辑、权限陷阱、网络代理配置以及高阶环境打包方案。

---

## 一、 高阶终端指令速查字典 (Docker篇)

> These instructions must be integrated into muscle memory to deal with the lowest-level issues of development.

### 1.1 磁盘空间、镜像与容器生命周期管理

在进行机器人高频开发和大规模仿真时，磁盘空间极易爆满，必须熟练掌握以下存储与对象管理指令。

* **空间画布透视（查看整体占用）**：

```bash
# 查看 Docker 磁盘占用的整体大盘（镜像、容器、数据卷各占多少，多少可回收）
docker system df

```

* **镜像（Images）深度控制（查看大小与删除）**：

```bash
# 【查看镜像空间】列出本地所有已下载或构建的静态镜像模板（含 ID、版本、SIZE 真实占用大小）
docker images

# 【删除镜像】根据 IMAGE ID 彻底删除某个不再需要的静态镜像模板（删除前需确保无容器依赖它）
docker rmi <IMAGE_ID>

```

> 💡 **防爆空间细节**：通过 `docker load -i xxx.tar.gz` 成功导入镜像到本地后，该镜像便已被完整解压并注册到 Docker 本地数据库。**原始的 `.tar.gz` 归签包可以立即安全删除**，完全不会影响后续容器的创建与运行。

* **安全垃圾回收（Prune 系列）**：

```bash
# 【容器清理】安全删除所有已经停止运行的容器，释放其写层空间（不影响运行中的容器）
docker container prune

# 【镜像清理】删除所有“悬空”（无标签/Dangling）的临时镜像层
docker image prune

# 【终极清理】删除所有未使用的容器、镜像、网络，并强制连带未挂载的数据卷（Volumes）一并物理拔除！
docker system prune -a --volumes

```

* **容器生命周期二次唤醒（查看可写层、删除容器）**：

```bash
# 【查看运行中】列出当前正在运行的容器
docker ps

# 【查看所有】列出系统内所有的容器（包含已经停止 Exited 的容器）
docker ps -a

# 【查看容器真实空间占用】列出所有容器，并额外显示每个容器独有的“写层（SIZE）”与虚拟大小（virtual size）物理空间占用
docker ps -as

# 【唤醒】一键拉起已停止的容器（先赋显示权限）
xhost +local:docker
docker start kuavo_container

# 【钻入】以 Zsh 终端身份钻入正在运行的后台容器（推荐）
docker exec -it kuavo_container zsh

# 【钻入】以 Bash 身份钻入正在运行的后台容器（备用）
docker exec -it kuavo_container /bin/bash

# 【物理删除容器】删除某个特定的容器（必须先停止该容器，此操作会彻底释放其临时写层，绝对不会删掉底层的静态镜像）
docker rm <CONTAINER_ID_or_NAME>

# 【强制删除容器】强行物理删除一个正在运行的容器
docker rm -f <CONTAINER_ID_or_NAME>

```

> 💡 **SIZE 字段的瘦身内幕**：运行 `docker ps -as` 时，`SIZE` 栏代表容器的**可写层（Writable Layer）增量大小**。当你在容器里跑仿真、积攒了几十 GB 的 `coredumps` 和日志后，这里的数字会极度膨胀。执行 `docker rm -f <容器名>` 能够**物理抹除该可写层的全部垃圾**，瞬间收回数十 GB 的空间，而底层的只读镜像和宿主机上挂载的代码文件绝对不会丢失。

### 1.2 Docker 深度交互与挂载逻辑控制

这些指令是开发者深入容器底层、解决挂载冲突和环境隔离的最强武器。

#### 1. 运行状态与挂载寻踪（诊断位）

在调试多个工作空间映射时，首先确认“我在哪”以及“物理路径在哪”。

```bash
# 【透视】核心：像 X 光片一样，透视容器到底挂载了宿主机的哪个文件夹
# 过滤掉干扰项，直接定位 Source 物理路径
docker inspect <容器ID或名字> | grep -C 5 "Source" | grep -v "/dev"

```

#### 2. 宿主机与容器的“跨空搬运”（数据位）

无需通过 Git 或 U 盘，直接在两个物理隔离的文件系统间传输权重模型或日志。

```bash
# 从容器往外拿（例：提取训练日志到宿主机）
docker cp <容器名>:/root/fast_lio_ws ~/

# 往容器里送（例：把新炼好的 ONNX 模型送入部署 environment）
docker cp ~/my_file.txt <容器名>:/root/

```

#### 3. 开发环境的一键起航（启动位）

针对 Kuavo 机器人的不同场景，选择最合适的进入方式。

```bash
# A. 官方快捷方式（依赖仓库内的脚本）
xhost +local:docker
./docker/run.sh

# B. 【推荐】手动全功率模式（暴力拆解挂载逻辑，强制开启 GPU 和显示投影）
xhost +local:docker
docker run -it  \
    --name kuavo_container \
    --gpus all \
    --privileged \
    --network host \
    --env="DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/root/kuavo_ws \
    kuavo_opensource_mpc_wbc_img:1.3.0 \
    zsh

# C. 【高阶长久防爆版】代码与数据分离挂载模式（推荐：将高频垃圾剥离至宿主机 /tmp 目录下）
docker run -it \
    --name kuavo_container \
    --gpus all \
    --privileged \
    --network host \
    --env="DISPLAY" \
    --env="ROS_LOG_DIR=/root/.ros/log" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/root/kuavo_ws:rw \
    -v /tmp/kuavo_cache:/root/.cache \
    -v /tmp/kuavo_ros_logs:/root/.ros/log \
    kuavo_opensource_mpc_wbc_img:1.3.0 \
    zsh

# D. 【终极双容器日志分流版】大日志目录统一管理形态（适用于常规仿真与强化学习多容器并行）
# 容器 1（常规仿真容器 kuavo_container）：
docker run -it \
    --name kuavo_container \
    --gpus all \
    --privileged \
    --network host \
    --env="DISPLAY" \
    --env="ROS_LOG_DIR=/root/.ros/log" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/root/kuavo_ws:rw \
    -v /tmp/kuavo_cache:/root/.cache \
    -v /tmp/kuavo_logs/kuavo_sim_logs:/root/.ros/log \
    kuavo_opensource_mpc_wbc_img:1.3.0 \
    zsh

# 容器 2（强化学习部署容器 kuavo_rl_deploy_container）：
docker run -it \
    --name kuavo_rl_deploy_container \
    --gpus all \
    --privileged \
    --network host \
    --env="DISPLAY" \
    --env="ROS_LOG_DIR=/root/.ros/log" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/root/kuavo_ws:rw \
    -v /tmp/kuavo_rl_cache:/root/.cache \
    -v /tmp/kuavo_logs/kuavo_rl_logs:/root/.ros/log \
    kuavo_opensource_mpc_wbc_img:1.3.0 \
    zsh

```

### 1.3 容器网络代理配置

```bash
# Clash 打开允许局域网连接，注入代理环境变量
export http_proxy=http://172.17.0.1:7890
export https_proxy=http://172.17.0.1:7890

# 取消代理
unset http_proxy https_proxy

```

### 1.4 Docker 内部垃圾定点清理高阶指南（日志、Core Dumps、编译缓存）

在进行机器人开发和算法高频调试时，容器内部极易堆积大量的冗余数据。如果在启动时没有做好分离挂载，必须定期进行容器内的“定点清理”。

* **全面排查大文件（容器内运行）**：

```bash
# 统计包含隐藏目录在内的所有文件和文件夹，并按大小排序，精确定位空间占用
du -ah /root | sort -rh | head -n 20

```

* **精准清除指令集（容器内运行）**：

```bash
# 1. 清理 ROS 运行日志（强清容器内部因高频通信产生的堆积日志）
sudo rm -rf /root/.ros/log/*

# 2. 清理核心转储文件（程序崩溃生成的 coredumps 记录，通常包含巨量非必要数据）
rm -rf /root/.ros/coredumps/*

# 3. 清理 Pip 安装包缓存与编译缓存（下次构建会自动重建，安全性高）
rm -rf /root/.cache/pip/*
rm -rf /root/.ccache/*

```

* **自动化静默清理别名（写入容器内 `/root/.zshrc` 或 `.bashrc`）**：

```bash
# 使用绝对路径绕过 rm 别名拦截，加 2>/dev/null 屏蔽因空目录产生的报错提示
alias clean_ros='/usr/bin/rm -rf /root/.ros/log/* /root/.ros/coredumps/* 2>/dev/null'

```

* **宿主机侧一键定向清理日志（安全防呆法）**：
在实现了多点大日志文件夹分类挂载后，清理工作可完全移步至**宿主机终端**执行，无需进入容器内部：
```bash
# 【一键彻底清空】清空两大容器的全部历史日志，保持目录结构完好
rm -rf /tmp/kuavo_logs/kuavo_sim_logs/* /tmp/kuavo_logs/kuavo_rl_logs/*

# 【精准定点清除】只清除常规仿真容器产生的日志
rm -rf /tmp/kuavo_logs/kuavo_sim_logs/*

```


> ⚠️ **安全红线**：末尾必须带有 `/*`，这代表仅清空文件夹内部的内容。如果丢失了 `/*` 将文件夹本体删除，容器内部程序写入日志时由于找不到外部关联物理路径会引发挂载中断报错。


* **⚠️ 存储层释放特性警示**：由于 Docker 采用分层结构，在容器内执行 `rm` 只是在当前可写层添加了逻辑“删除标记”，宿主机的磁盘物理空间可能不会立刻释放。若想最彻底地清除这些“增量垃圾”，在确保核心代码已安全同步的情况下，可直接在宿主机执行 `docker rm kuavo_container`，这能瞬间物理回收其对应的全部可写层空间。

---

## 二、 核心辨析：镜像（Image）与容器（Container）的本质区别

这是避免开发环境误删、建立正确容器化数据流的核心基石。

### 2.1 镜像与容器深度特性对照

| 特征维度 | 镜像 (Image) | 容器 (Container) |
| --- | --- | --- |
| **底层类比** | 软件安装包、面向对象中的 **“类 (Class)”**、建筑图纸 | 运行中的程序实例、面向对象中的 **“对象 (Object)”**、实体房屋 |
| **可变状态** | **完全只读 (Read-Only)**，多容器共享同一底层 | **动态可写 (Writable Layer)**，专属的独立工作台 |
| **存储物理期** | 长期固化于宿主机存储内，属于环境基底 | 属于生命周期实体，随着 `run`, `start`, `rm` 变化 |
| **误删数据波及** | 包含原始 ROS 环境与驱动，删除它相当于卸载大环境 | 删掉容器只会卷走运行产生的临时增量，**绝不会反噬底层的镜像** |

### 2.2 核心机制：写时复制（Copy-on-Write）与多容器共享

* **多容器并存定理**：Docker 支持**无限多个不同的容器同时挂载运行同一个基础镜像**。例如，常规控制算法容器 `kuavo_container` 与强化学习容器 `kuavo_rl_deploy_container` 可以并存在系统内，同时读取 `kuavo_opensource_mpc_wbc_img:1.3.0` 镜像的基础底座。
* **数据结界隔离**：基于写时复制技术，所有容器共享这 8.47GB 的只读基础层，而每个容器在启动时会被赋予专属的极轻量“可写层”。你在容器 A 里面对系统工具和依赖的任何添置或改写，绝对不会干扰到容器 B，更不会污染到基础镜像模板。
* **无痕开发重置体验**：若因为安装非官方小工具（如 `tmux`, `htop`）或者 Python 三方库导致依赖错乱冲突，只需一行 `docker rm -f`，然后再用同一镜像秒级创建一个新容器，系统瞬间还原到最纯净的官方初始状态。

---

## 三、 Docker 核心基石：Namespaces 与 Cgroups

* **Namespaces（命名空间）**：Docker 的“障眼法”。它让容器内的进程以为自己拥有独立的 PID（进程号 1）、独立的网络接口和独立的文件系统。你在 Docker 里看到的 `/`（根目录），其实只是宿主机硬盘深处（`/var/lib/docker/overlay2/`）的一个普通文件夹。
* **Cgroups（控制组）**：Docker 的“紧箍咒”。它限制这个容器最多只能用宿主机（如笔记本电脑）有多少 CPU 核心和多少内存。

---

## 四、 挂载逻辑（Volume Mounting）：跨越次元的传送门

Docker 容器一旦销毁，里面的数据就会灰飞烟灭（无状态化）。为了保留代码，必须使用挂载。

* **映射指令**：`-v ~/kuavo-ros-opensource:/root/kuavo_ws`
* **底层机制（Bind Mount）**：Docker 强制将容器内的 `/root/kuavo_ws` 目录的 inode 指针，强行指向宿主机的 `~/kuavo-ros-opensource`。
* **唯一入口铁律**：容器启动时，入口就已经焊死。如果你在宿主机把代码放在了 `kuavo-clean`，而容器挂载的是 `kuavo-ros-opensource`，那么容器内部绝无可能看到 `kuavo-clean` 里的东西。这就好比投影仪只能照着一张幻灯片。

### 4.1 高频硬核玩法：多文件夹多点映射定理

Docker 支持在同一次启动命令中使用任意数量的 `-v` 参数，建立多条跨越层级的物理通道。

* **物理规律：一向多可拓，多向一必冲**：
* **允许【一个外部物理路径 $\rightarrow$ 映射到容器内部多个节点】**：例如把宿主机的通用配置文件夹，同时插到容器内的不同路径。
* **禁止【多个外部物理路径 $\rightarrow$ 映射到容器内部同一个节点】**：如果在启动时写入多个不同的宿主机目录去对齐同一个容器内部的路径（例如连续映射两个代码目录给 `/root/kuavo_ws`），后挂载的文件夹会强行遮挡前面的挂载源，导致文件发生丢失错觉。


* **长效编译保存机制**：因为使用了 `-v $(pwd):/root/kuavo_ws` 通道，你在容器中运行编译产生的 `build/` 和 `devel/` 文件夹实际上是**跨越次元直接写在宿主机硬盘上的**。所以，哪怕你将当前的 Docker 容器完全删除并重新添加，这些编译出来的核心固件依然会安稳地留在宿主机里，新容器启动后可直接 `source` 运行，**完全不需要重新编译**。

---

## 五、 权限错位综合征：那个讨厌的“红色小锁”

这是 Docker 与宿主机文件系统交互时最常见的陷阱。

* **身份的割裂**：
* **宿主机（外界）**：你是普通用户 `$USER`，系统底层身份代码为 `UID 1000`。
* **Docker（内部）**：你是超级管理员 `root`，身份代码为 `UID 0`。


* **锁的诞生**：当你在 Docker 内部执行 `catkin_make` 或 `touch` 创建文件时，Linux 内核会把这些文件的拥有者标记为 `UID 0`。当你回到宿主机图形界面，Ubuntu 发现你是 `UID 1000`，为了保护 `root` 的财产，直接给你挂上红锁，甚至拒绝刷新文件夹内容（导致“文件消失”的错觉）。
* **终极解药**：永远记得在宿主机使用 `sudo chown -R $USER:$USER <目录>` 把文件的所有权抢回来。

---

## 六、 高阶进阶：Docker 开发环境与项目打包

不仅要在无菌环境里开发，还要能把自己的成果打包成“数字集装箱”，发给任何人都能一键运行。

### 6.1 方案 A：使用 Dev Containers 进行“无痕开发”

让 VS Code 直接在容器里写代码，本机无需安装复杂环境（如 ROS 2）：

1. 本机安装 Docker，并在 VS Code 中安装 **Dev Containers** 插件。
2. 在项目根目录按 `Ctrl+Shift+P`，搜索 `Dev Containers: Add Dev Container Configuration Files` -> 选择所需环境（如 `ROS 2 Humble`）。
3. 点击弹出的 **"Reopen in Container"**。代码补全和编译都在容器内完成，与本机彻底隔离。

### 6.2 方案 B：将自己的项目打包成发行镜像（核心发版能力）

当你的项目写完了，想部署到实车或者发给别人展示，请在你工作空间的根目录下，新建一个 `Dockerfile`：

```dockerfile
# 1. 声明底层环境 (自带 ROS 2 Humble)
FROM osrf/ros:humble-desktop

# 2. 设置容器内的工作目录
WORKDIR /my_robot_ws

# 3. 把你当前电脑的源码 (src) 拷贝到镜像里
COPY src/ ./src/

# 4. 安装属于你项目的特定依赖
RUN apt-get update && rosdep update && \
    rosdep install --from-paths src --ignore-src -y

# 5. 编译你的项目 (注意：要先 source 一下系统 ROS 2 环境)
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# 6. 配置启动脚本 (ENTRYPOINT)
# 这一步保证了别人一旦 run 这个镜像，环境就已经挂载好了
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /my_robot_ws/install/setup.bash" >> ~/.bashrc

# 7. 默认执行的命令 (可选项，比如启动你的主节点)
# CMD ["ros2", "launch", "my_package", "main.launch.py"]

```

**打包与导出分享指令：**

```bash
# 构建你自己的镜像 (打上 v1.0 标签)
docker build -t my_robot_project:v1.0 .

# 将镜像导出为压缩包，用 U 盘拷给任何人！
docker save -o my_robot_project_v1.0.tar my_robot_project:v1.0

# 别人拿到压缩包后的加载与运行命令：
docker load -i my_robot_project_v1.0.tar
docker run -it --net=host my_robot_project:v1.0 /bin/bash

```

---

## 七、 实战案例复盘 —— Docker 内外的相对论

* **案情**：在宿主机终端输入 `cd ~/fast_lio_ws/src` 报错“没有该目录”。
* **排查**：`fast_lio_ws` 是在 Docker 容器最上层的私有读写层中创建的，并未通过 `-v` 映射到宿主机。宿主机的 `~` 与 Docker 容器内的 `/root/` 不是同一目录。
* **破局**：理解“内外结界”。对于未挂载的纯容器内部数据，必须钻入容器 (`docker exec`) 才能访问；或者使用 `docker cp` 将其提取到宿主机。