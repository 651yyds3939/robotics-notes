# Ubuntu CPU 限频与控温完整笔记（20.04 / 22.04）

> 适用方向：AMD 移动处理器、ROS / Gazebo 等持续负载。以下以 Ryzen 7 5800H、最高频率目标 3.2GHz 为示例。  
> 本文保留旧版 Ubuntu 20.04 控温方案，并补充 Ubuntu 22.04 使用 `amd-pstate-epp` 的新方案。**先识别当前驱动，再选择操作方法；不要将两套命令混用。**

## 目录

1. 控温目标与原理
2. 判断当前 Ubuntu 系统使用哪套方案
3. 方案 A：旧版 Ubuntu 20.04 / `acpi-cpufreq`（保留原方案）
4. 方案 B：Ubuntu 22.04 / `amd-pstate-epp`（新增）
5. 两套方案的区别
6. 温度监控、常见问题与注意事项
7. 参考资料

---

## 一、控温目标与基本原理

在运行 Gazebo、ROS / ROS2、RViz、编译或长时间仿真任务时，希望：

- 避免 CPU 长时间处于较高频率和功耗状态，降低高温及风扇噪声。
- 在性能可接受的情况下，将 CPU 最高频率控制在 **3.2GHz** 左右。
- 保留 CPU 在空闲时根据负载自动降低频率的能力（新方案尤其如此）。
- 让设置在每次开机后自动执行，并支持随时恢复。

### 为什么限频能降低温度？

AMD Ryzen 7 5800H 的基础频率为 3.2GHz，最高加速频率可达约 4.4GHz。较高频率往往伴随更高的功耗和发热，但**频率下降幅度不等于温度或性能下降幅度**，具体要看工作负载、散热与功耗控制。

另外，CPU 温度高不一定都是 Boost 造成的。散热器积灰、散热材料、环境温度和风扇曲线同样会影响温度。

---

## 二、先检查当前驱动（两套系统均可使用）

```bash
# 系统版本
lsb_release -a

# 内核版本
uname -r

# CPU 型号
grep -m1 'model name' /proc/cpuinfo

# CPU 频率驱动
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver

# 支持的 governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors

# AMD P-State 当前模式（如果存在）
cat /sys/devices/system/cpu/amd_pstate/status 2>/dev/null || true

# 全局 Boost 开关是否存在
ls -l /sys/devices/system/cpu/cpufreq/boost 2>/dev/null || true
```

**如何选择：**

| 检查结果 | 建议方法 |
| --- | --- |
| `acpi-cpufreq`，并且存在 `/sys/devices/system/cpu/cpufreq/boost` | 使用方案 A |
| `amd-pstate-epp` 且 `/sys/devices/system/cpu/amd_pstate/status` 为 `active` | 使用方案 B |
| 驱动或接口与上述不同 | 先检查实际可用接口，不要直接套用脚本 |

**注意：** Ubuntu 版本号并不直接决定 CPU 驱动。相同发行版也可能因 Linux 内核、BIOS 和启动参数不同而使用不同驱动。

---

## 三、方案 A：旧版 Ubuntu 20.04 / `acpi-cpufreq`（原方案保留）

> 这一节保留此前的“关闭 Boost + 限制最高频率 + 可选最低频率 + powersave”完整方法。仅在相应接口存在、驱动支持时执行。

### 3.1 问题背景（旧方案）

在某些使用传统 ACPI 频率管理的笔记本上：

- Boost 允许 CPU 在负载较高时冲到 4GHz 左右或更高。
- 在原先的 Gazebo 场景中，曾观察到 CPU 温度接近 95～100°C、风扇噪声较大。
- 对于该旧驱动环境，单独用 `cpufreq-set -u` 限频可能不足以达到预期的 Boost 控温效果，因此旧方案同时显式关闭 Boost。

不要把“`cpufreq-set -u` 在任何 Linux 系统上都不能限制 Boost”当作通用规律；行为取决于实际驱动。

### 3.2 安装工具（如果尚未安装）

```bash
sudo apt update
sudo apt install cpufrequtils -y
```

### 3.3 关闭 CPU Boost

```bash
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

检查：

```bash
cat /sys/devices/system/cpu/cpufreq/boost
```

输出 `0` 代表旧接口报告 Boost 已关闭。如果文件不存在，请勿在该系统继续执行此方案。

### 3.4 设置最高频率 3.2GHz

```bash
sudo cpufreq-set -r -u 3.2GHz
```

### 3.5 设置最低频率 1.8GHz（原方案，可选）

```bash
sudo cpufreq-set -r -d 1.8GHz
```

这条命令**不是控温必需项**。提高最低频率可能减少空闲时的降频空间；如果追求待机功耗更低，可以不设置这一步。

### 3.6 设置 governor 为 powersave（原方案）

```bash
sudo cpufreq-set -r -g powersave
```

查看可用选项：

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
```

### 3.7 验证频率（原方法）

```bash
watch -n 1 "cat /proc/cpuinfo | grep MHz"
```

也可以检查调频策略上限：

```bash
for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    echo "$(basename "$policy"): $(cat "$policy/scaling_max_freq") kHz"
done
```

### 3.8 旧方案曾记录的实际效果

| 项目 | 优化前 | 优化后 |
| --- | --- | --- |
| CPU 频率 | 3.9～4.0GHz | 3.0～3.2GHz |
| CPU 温度 | 95～100°C | 75～85°C |
| 风扇噪声 | 较大 | 明显降低 |
| Gazebo 帧率 | 正常 | 基本无影响 |

以上是特定测试场景的历史记录，**并非所有电脑或 Gazebo 项目都能获得相同结果**。

### 3.9 一键执行（原方案保留）

```bash
# 仅适用于存在旧 Boost 接口的系统
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
sudo cpufreq-set -r -u 3.2GHz
sudo cpufreq-set -r -d 1.8GHz
sudo cpufreq-set -r -g powersave
```

### 3.10 原方案：使用 systemd 开机自动设置

**第 1 步：创建脚本**

```bash
sudo nano /usr/local/bin/cpu-limit.sh
```

内容（保留原方案的四项设置）：

```bash
#!/bin/bash
set -e

echo 0 > /sys/devices/system/cpu/cpufreq/boost
cpufreq-set -r -u 3.2GHz
cpufreq-set -r -d 1.8GHz
cpufreq-set -r -g powersave
```

**第 2 步：赋予权限**

```bash
sudo chmod +x /usr/local/bin/cpu-limit.sh
```

**第 3 步：创建服务**

```bash
sudo nano /etc/systemd/system/cpu-limit.service
```

下面保留原笔记的 service 写法：

```ini
[Unit]
Description=CPU Limit Service
After=multi-user.target

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 5
ExecStart=/usr/local/bin/cpu-limit.sh

[Install]
WantedBy=multi-user.target
```

> 维护提示：原配置中的 `After=multi-user.target` 与 `WantedBy=multi-user.target` 同时存在，可能产生不合理的启动顺序依赖。实际使用时**推荐删除 `After=multi-user.target` 这一行**，保留其他原方案命令不变。无需为了限频固定睡眠 5 秒，但原来的延迟设置可以继续保留。

**第 4 步：重新加载、启用和启动**

原笔记命令如下（`daemon-reexec` 通常不是必需的）：

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable cpu-limit.service
sudo systemctl start cpu-limit.service
```

**第 5 步：检查**

```bash
systemctl status cpu-limit.service
cat /sys/devices/system/cpu/cpufreq/boost
```

`status=0/SUCCESS` 代表脚本完成；Boost 接口读出 `0` 代表已关闭 Boost。

**第 6 步：禁用与恢复**

原笔记保留的命令：

```bash
sudo systemctl disable cpu-limit.service
```

但要注意：`disable` 仅取消**未来开机自动启动**，不会恢复当前频率或 Boost 状态。更完整的恢复方式是：

```bash
sudo systemctl disable --now cpu-limit.service
sudo reboot
```

重启后由系统默认驱动及其他电源管理工具重新管理频率。若有其他脚本也改过调频设置，则需要一并检查。

### 3.11 旧方案常见问题

**限频后仍看到 4GHz？** 检查 Boost 是否真的关闭、当前驱动和实际 governor；也要确认是否被其他工具重新设置。

**`cpufreq-set` 报错？** 检查是否安装 `cpufrequtils`、是否使用 `sudo`、驱动是否支持相应操作。

**governor 设置无效？** 通过 `scaling_available_governors` 检查可用策略，必要时检查其他电源管理服务。

---

## 四、方案 B：Ubuntu 22.04 / `amd-pstate-epp`（新增）

> 已验证的示例环境：Linux 6.8、`amd-pstate-epp` 驱动、AMD P-State `active` 模式，传统全局 Boost 接口不存在。通过各个 `policy*/scaling_max_freq` 限制上限到 **3200000 kHz（3.2GHz）**。

### 4.1 为什么不能直接使用方案 A？

在 `amd-pstate-epp` / `active` 模式下，CPU 性能管理主要使用 AMD CPPC 与 EPP（Energy Performance Preference）。这套环境没有旧路径 `/sys/devices/system/cpu/cpufreq/boost`，所以原方案第一条会报“没有那个文件或目录”。

**新方案只限制 CPU 调频策略的最高频率，不声称已经关闭硬件层面的 Boost。** 硬件仍根据负载、温度、功耗和 EPP 偏好调节实际性能。

### 4.2 检查驱动、频率范围和 EPP

```bash
# 当前驱动
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver

# AMD P-State 状态
cat /sys/devices/system/cpu/amd_pstate/status

# 调频范围（单位 kHz）
for name in cpuinfo_min_freq cpuinfo_max_freq scaling_min_freq scaling_max_freq; do
    printf '%s: ' "$name"
    cat "/sys/devices/system/cpu/cpu0/cpufreq/$name"
done

# EPP 偏好
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference

# Boost 旧路径是否存在
ls /sys/devices/system/cpu/cpufreq/boost 2>/dev/null || echo '旧 Boost 接口不存在'
```

可能看到类似：

```text
amd-pstate-epp
active
cpuinfo_min_freq: 400000
cpuinfo_max_freq: 4463000
scaling_min_freq: 400000
scaling_max_freq: 4463000
performance
旧 Boost 接口不存在
```

上述数值是示例，不代表所有处理器都相同。

### 4.3 临时限频：全部 CPU 最高 3.2GHz

```bash
for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    echo 3200000 | sudo tee "$policy/scaling_max_freq"
done
```

每个 `3200000` 表示一次写入成功；若输出 `Invalid argument` 或 `Permission denied`，不要直接进行下一步，先排查驱动与允许的频率范围。

### 4.4 立即验证所有 CPU 策略

```bash
for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    echo "$(basename "$policy"): $(cat "$policy/scaling_max_freq") kHz"
done
```

预期每行的上限均为：

```text
policy0: 3200000 kHz
policy1: 3200000 kHz
...
```

对 8 核 16 线程的机器，可能出现 16 个 `policy`；实际以系统列出的策略数量为准。

### 4.5 新方案为什么不设置最低频率与 powersave？

- 不修改 `scaling_min_freq`：保留当前默认最低频率，让 CPU 空闲时仍有降频空间。
- 不强制改变 governor：先只改变最高频率，便于观察 Gazebo 的温度和性能变化。
- 保留 EPP 原有值（例如 `performance`）：EPP 是性能与能效偏好提示，和最高频率上限不是同一个参数。

### 4.6 创建新方案的开机限频脚本

```bash
sudo nano /usr/local/bin/cpu-limit.sh
```

写入：

```bash
#!/bin/bash
set -e

# Ubuntu 22.04 / amd-pstate-epp
# 目标：限制 CPU 调频策略最高频率为 3.2GHz

MAX_FREQ=3200000

for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    [ -d "$policy" ] || continue
    echo "$MAX_FREQ" > "$policy/scaling_max_freq"
    echo "$(basename "$policy"): max frequency set to 3.2GHz"
done

echo "CPU frequency limit applied: 3.2GHz"
```

> 此脚本不访问缺失的 Boost 接口，也不修改最低频率及 EPP。它假设系统确实存在 `policy*` 并允许写入 `3200000`；请务必先完成 4.3～4.4 的手动测试。

保存后：

```bash
sudo chmod +x /usr/local/bin/cpu-limit.sh
sudo /usr/local/bin/cpu-limit.sh
```

### 4.7 创建 systemd 服务

```bash
sudo nano /etc/systemd/system/cpu-limit.service
```

写入：

```ini
[Unit]
Description=CPU Frequency Limit (3.2GHz)

[Service]
Type=oneshot
ExecStart=/usr/local/bin/cpu-limit.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

### 4.8 开启开机自启动并立即应用

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cpu-limit.service
```

检查：

```bash
systemctl status cpu-limit.service
systemctl is-enabled cpu-limit.service
systemctl is-active cpu-limit.service
```

成功时，通常会出现：

```text
Loaded: ... enabled
Active: active (exited)
status=0/SUCCESS
```

`active (exited)` 对 `Type=oneshot` 且 `RemainAfterExit=yes` 的服务来说是正常的：脚本已执行完毕，不需要常驻进程。

### 4.9 重启并验证自动限频

```bash
sudo reboot
```

重启后：

```bash
# 1. 服务是否启用
systemctl is-enabled cpu-limit.service
systemctl is-active cpu-limit.service

# 2. 是否全部保持 3.2GHz 上限
for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    echo "$(basename "$policy"): $(cat "$policy/scaling_max_freq") kHz"
done
```

若输出为 `enabled`、`active`，且所有策略均为 `3200000 kHz`，说明**开机自动限频已在重启后生效**。仅有 `active (exited)` 不能证明频率没有被别的服务覆盖，应以频率读回值为准。

### 4.10 临时重新应用或恢复默认

重新应用当前脚本：

```bash
sudo systemctl restart cpu-limit.service
```

停用自动限频，并通过重启恢复系统默认管理：

```bash
sudo systemctl disable --now cpu-limit.service
sudo reboot
```

注意：`disable --now` 不会自动撤销已写入的运行时上限。重启后应再读一次 `scaling_max_freq`，确认由系统默认电源管理策略接管。

以后要重新启用：

```bash
sudo systemctl enable --now cpu-limit.service
```

### 4.11 新方案常见问题

**为什么看不到 Boost 文件？** 在本示例内核和 `amd-pstate-epp` 配置下，传统全局 Boost 路径不存在；这是接口差异，并不意味着 CPU 损坏。

**为什么上限是 3.2GHz，监控频率偶尔有偏差？** `scaling_max_freq` 是调频框架的策略上限，不是硬件功耗墙；不同监控工具的测量口径也不完全相同。若持续明显超出，请检查驱动与其他调频工具。

**为什么开机后上限恢复了？** 检查服务日志及 TLP、auto-cpufreq、power-profiles-daemon 等电源管理软件是否在之后修改设置。

```bash
journalctl -u cpu-limit.service -b --no-pager
```

**如果 `echo 3200000` 报错怎么办？** 检查驱动、策略上下限和内核是否支持该值，不要强行写不存在的接口，也不要直接照搬其他电脑的 `cpuinfo_max_freq`。

---

## 五、两套方案对比

| 项目 | 方案 A：旧版 `acpi-cpufreq` | 方案 B：`amd-pstate-epp` |
| --- | --- | --- |
| 核心思路 | 关闭 Boost，再限制频率 | 设置 CPU 调频策略上限 |
| Boost 接口 | 使用全局 `/cpufreq/boost` | 本示例不存在该接口 |
| 最高频率 | 3.2GHz | 3.2GHz |
| 最低频率 | 原笔记可选 1.8GHz | 保留系统默认值 |
| governor | 原笔记设为 `powersave` | 不强制更改 |
| EPP | 通常不涉及 | 保留默认偏好 |
| 开机自动执行 | systemd | systemd |
| 是否已做温度实测 | 有历史 Gazebo 记录 | 需要在相同负载下验证 |

**结论：** 同一颗 CPU 采用不同方法，根源通常在于 **Linux 内核的 CPU 调频驱动与支持的控制接口不同**，而不是“Ubuntu 20.04 与 22.04 必然规定两种固定方法”。

---

## 六、温度与性能监控

安装工具：

```bash
sudo apt update
sudo apt install lm-sensors -y
```

查看温度：

```bash
sensors
```

持续查看温度：

```bash
watch -n 1 sensors
```

持续查看报告的 CPU 频率：

```bash
watch -n 1 "grep 'cpu MHz' /proc/cpuinfo"
```

建议在**相同 Gazebo 场景、相近室温、相同风扇与电源模式**下对比：

1. CPU 温度（稳定运行几分钟后的区间）。
2. CPU 实际频率、风扇噪声。
3. Gazebo 实时因子（RTF）与仿真帧率。
4. 编译等 CPU 密集任务是否明显变慢。

频率限制可以改善某些负载下的散热，但不会修复积灰、散热硅脂老化、风扇故障等物理问题。

---

## 七、日常命令速查

```bash
# 查看驱动
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver

# 查看单个调频策略的上限
cat /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq

# 查看全部策略的上限
for policy in /sys/devices/system/cpu/cpufreq/policy*; do
    echo "$(basename "$policy"): $(cat "$policy/scaling_max_freq") kHz"
done

# 查看限频服务
systemctl status cpu-limit.service

# 再次执行脚本
sudo systemctl restart cpu-limit.service

# 取消开机自启动（不会立即还原当前限制）
sudo systemctl disable --now cpu-limit.service
```

> **最后总结：** 旧环境优先沿用原来的“关 Boost + 限频”方案；新环境优先使用 `amd-pstate-epp` 的策略上限方案。以驱动检查结果和重启后实际读回结果为准，别只凭 Ubuntu 版本判断。

## 八、参考资料

- Linux Kernel 6.8 文档：AMD P-State CPU 性能管理 — https://www.kernel.org/doc/html/v6.8/admin-guide/pm/amd-pstate.html
- Linux Kernel 文档：CPUFreq 频率管理 — https://www.kernel.org/doc/html/latest/admin-guide/pm/cpufreq.html

