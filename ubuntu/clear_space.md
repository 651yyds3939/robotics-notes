````markdown
# 🧠 Ubuntu 磁盘空间查看与清理指南（终端版）

> 适用于：日常开发 / ROS / 仿真 / 深度学习环境  
> 目标：快速定位磁盘占用 + 安全高效清理

---

# 📊 一、查看磁盘空间（全局）

## 1️⃣ 查看磁盘分区使用情况
```bash
df -h
````

### 📌 重点字段说明：

* `Filesystem`：设备（如 /dev/sda1）
* `Size`：总容量
* `Used`：已使用
* `Avail`：剩余空间
* `Use%`：使用率
* `Mounted on`：挂载点

### 🎯 重点关注：

* `/` → 系统盘
* `/home` → 用户数据
* `/media` → 外接设备 / 挂载分区

---

## 2️⃣ 查看 inode（文件数量占用）

```bash
df -i
```

👉 有时候不是空间满，而是文件数用完

---

# 📦 二、查看目录占用（定位“谁吃空间”）

## 1️⃣ 当前目录占用情况

```bash
du -h --max-depth=1
```

👉 显示当前目录下每个子目录大小

---

## 2️⃣ 查看某个路径

```bash
du -h /home --max-depth=1
```

---

## 3️⃣ 快速排序找大文件夹

```bash
du -h --max-depth=1 | sort -rh
```

---

## 4️⃣ 查看单个目录总大小

```bash
du -sh ~/.ros
```

---

## 5️⃣ 查找最大文件（Top 20）

```bash
sudo du -h / | sort -rh | head -20
```

⚠️ 可能比较慢

---

## 6️⃣ 查找大文件（按大小）

```bash
find / -type f -size +500M
```

---

# 🧹 三、磁盘清理（安全操作）

---

## 🔥 1️⃣ ROS 清理（重点！！！）

### 清理日志（推荐）

```bash
rm -rf ~/.ros/log
```

---

### 使用官方工具（ROS1）

```bash
rosclean purge
```

自动确认：

```bash
rosclean purge -y
```

---

### 查看 ROS 占用

```bash
du -sh ~/.ros
```

---

## 🚀 2️⃣ ROS2 / 工作空间清理

进入项目目录：

```bash
cd ~/your_ros_workspace
```

清理构建文件：

```bash
sudo rm -rf ~/.ros/*        清理全部ros相关的日志之类的
rm -rf build install log

```

👉 可释放数 GB 空间

---

## 🧊 3️⃣ Cache 清理

```bash
rm -rf ~/.cache/*
```

👉 安全，可自动重建

---

## 📦 4️⃣ apt 包清理

清理无用依赖：

```bash
sudo apt autoremove
```

清理缓存：

```bash
sudo apt clean
```

---

## 🧪 5️⃣ pip 缓存清理

```bash
pip cache purge
```

或手动：

```bash
rm -rf ~/.cache/pip
```

---

## 🐳 6️⃣ Docker 清理（如果使用）

查看占用：

```bash
docker system df
```

清理：

```bash
docker system prune -a
```

---

## 🌍 7️⃣ 浏览器缓存

```bash
rm -rf ~/.cache/google-chrome
rm -rf ~/.mozilla/firefox/*.default-release/cache2
```

---

## 🤖 8️⃣ Gazebo 清理

```bash
rm -rf ~/.gazebo/*
```

---

## 🧠 9️⃣ Snap 清理

查看版本：

```bash
snap list --all
```

删除旧版本：

```bash
sudo snap remove <package> --revision=<old_version>
```

---

# ⚙️ 四、自动清理（推荐）

---

## 1️⃣ 创建清理脚本

```bash
nano ~/cleanup.sh
```

写入：

```bash
#!/bin/bash

echo "=== Cleanup Start $(date) ==="

rm -rf ~/.ros/log
rm -rf ~/.cache/*
rm -rf ~/.gazebo/*

echo "=== Cleanup Done ==="
```

---

## 2️⃣ 添加执行权限

```bash
chmod +x ~/cleanup.sh
```

---

## 3️⃣ 设置定时任务

```bash
crontab -e
```

### 每周清理一次（推荐）

```bash
0 3 * * 0 /home/你的用户名/cleanup.sh
```

### 每天清理（不太必要）

```bash
0 3 * * * /home/你的用户名/cleanup.sh
```

---

# 🧠 五、进阶技巧（防止再次爆炸）

---

## 1️⃣ 限制 ROS 日志位置

```bash
export ROS_LOG_DIR=/tmp/ros_logs
```

👉 重启自动清理

---

## 2️⃣ 实时监控磁盘

```bash
watch -n 1 df -h
```

---

## 3️⃣ 图形工具（可选）

```bash
baobab
```

---

# ⚠️ 六、注意事项

---

## ❗ 不要随便删除：

* `/usr`
* `/bin`
* `/lib`
* `/etc`

---

## ❗ `.ros` 删除原则：

* `log` → ✅ 可以删
* `.bag` → ⚠️ 谨慎（可能是重要数据）

---

## ❗ 运行中的程序：

👉 不要清理（可能导致崩溃）

---

# 🧾 七、总结

👉 磁盘占用大头通常是：

| 来源              | 特点      |
| --------------- | ------- |
| `.ros`          | 日志爆炸    |
| `build/install` | ROS构建产物 |
| `.cache`        | 缓存堆积    |
| Docker          | 镜像巨大    |

---

# 🚀 最常用组合（建议记住）

```bash
df -h
du -h --max-depth=1
du -sh ~/.ros
rm -rf ~/.ros/log
rm -rf ~/.cache/*
sudo apt autoremove
```

---

👉 一句话总结：

> **磁盘问题 = 找大户 + 删缓存 + 清日志**

---

