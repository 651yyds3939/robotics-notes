# Ubuntu 系统开机速度深度优化实战笔记

**设备环境**：Lenovo Legion R9000P (AMD Ryzen + RTX 3070)
**系统版本**：Ubuntu (与 Windows 双系统)
**初始开机耗时**：2分46秒 (2m 46.708s)
**最终开机耗时**：39.8秒 (其中核心系统启动仅需约 26 秒)

## 1. 故障排查 (精准定位病灶)
优化系统开机速度的第一步，是找出是谁在拖延时间。

* **查看总开机耗时分布：**
    ```bash
    systemd-analyze
    ```
    *说明：这能拆解出固件(firmware)、引导(loader)、内核(kernel)和用户空间(userspace)各自的耗时。*

* **列出最耗时的系统服务：**
    ```bash
    systemd-analyze blame
    ```

* **查看内核底层日志 (找隐藏的超时等待)：**
    ```bash
    dmesg | less
    ```
    *或者过滤错误信息：`dmesg | grep -iE "error|timeout|failed|warn"`*

---

## 2. 解决 Userspace (用户空间) 卡顿 90 秒问题

**现象**：`userspace` 耗时接近 2 分钟，但 `blame` 服务列表里的时间加起来根本对不上。
**病因**：系统在开机挂载阶段试图寻找一个**已经失效或被删除的 Swap（交换）分区**。由于找不到该硬盘分区，系统默认硬卡 90 秒直到超时放弃。

**解决办法**：
1.  打开磁盘挂载配置文件：
    ```bash
    sudo nano /etc/fstab
    ```
2.  找到失效的 Swap 配置行（例如带有旧的 `UUID` 且类型为 `swap` 的行），在行首加上 `#` 将其注释掉。
3.  保存并退出 (按 `Ctrl+O` 写入，`Enter` 确认，`Ctrl+X` 退出)。

---

## 3. 解决 Kernel (内核) 卡顿 30 秒问题

**现象**：修复上一步后，内核加载依然需要 33 秒，通过 `dmesg` 日志发现中间有整整 30 秒的“时间跳跃/空白”。
**病因**：`initramfs` (内核初始化内存盘) 的配置中，仍然记录着那个旧 Swap 分区的 UUID。内核在极早期的启动阶段，试图从那个不存在的硬盘分区中**恢复休眠状态 (Resume)**，默认超时等待 30 秒。

**解决办法**：
1.  强制告诉内核不要从任何分区恢复休眠状态：
    ```bash
    echo "RESUME=none" | sudo tee /etc/initramfs-tools/conf.d/resume
    ```
2.  **关键步骤**：重新生成内核引导镜像，使修改彻底生效：
    ```bash
    sudo update-initramfs -u
    ```

---

## 4. 锦上添花：禁用不必要的自启服务

为了进一步压榨开机速度，可以关闭一些桌面用户根本不需要的等待服务。

* **禁用网络等待服务**（强制等连上网才进桌面，对个人电脑无意义）：
    ```bash
    sudo systemctl disable NetworkManager-wait-online.service
    ```
* **禁用老旧的 CPU 限制服务**（避免与现代主板调度冲突，节省 5 秒）：
    ```bash
    sudo systemctl disable cpu-limit.service
    ```

---

## 5. 总结对比

| 环节 | 优化前 | 优化后 | 解决关键 |
| :--- | :--- | :--- | :--- |
| **Kernel (内核)** | 33.2秒 | **2.1秒** | 禁用旧 Swap 休眠恢复 (`update-initramfs`) |
| **Userspace (用户空间)** | 1分56秒 | **24.2秒** | 在 `/etc/fstab` 中注释失效的挂载点 |
| **系统真实启动总时** | **2分29秒** | **约26.3秒** | **成功剔除了约 120 秒的“超时傻等”** |

*备注：`plymouth-quit-wait.service` 虽然在服务列表中耗时较长（20秒左右），但它是伴随桌面准备过程的开机动画服务，不造成真正的阻塞延迟，无需特别处理。*
