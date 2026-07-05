# OpenClaw —— 夹爪控制配置与行为树集成

> OpenClaw 是 Kuavo VLA 抓取管线中行为树的一个**叶子动作节点**，负责在抓取流程结束时张开夹爪释放物体。本笔记记录其配置要点、ROS 接口以及在机器人抓取闭环中的作用。

---

## 第 0 章：OpenClaw 在抓取管线中的位置

在行为树版 VLA 抓取流程（[22.2.tree_VLA_grasp](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/22.2.tree_VLA_grasp.md)）中，OpenClaw 是收尾节点：

```text
YOLO 检测 → TF2 坐标 → IK 逆解 → 曲肘 → 预瞄 → 水平插入 → CloseClaw（闭合抓取）
    → 抬升 → 肩膀外摆 75° → 曲肘收手 → OpenClaw（张开释放） → Init 复位
```

---

## 第 1 章：ROS 接口

### 1.1 服务调用

夹爪控制通过 ROS Service 下发：

```
服务名：/control_robot_leju_claw
类型：  kuavo_msgs/srv/controlLejuClaw
```

### 1.2 状态反馈

```
话题名：/leju_claw_state
内容：  当前夹爪位置（0-100）、电流、温度等
```

---

## 第 2 章：位置映射（以实机为准）

> ⚠️ **官方文档/注释有误**：部分旧文档和 `.h` 注释写的是 `0=闭合, 100=张开`，但底层 `liblejuclaw.a` 的实际行为**相反**。

| position 值 | 实际效果 |
|------------|---------|
| **0** | 夹爪张开到限位（`joint_end`） |
| **100** | 夹爪闭合到限位（`joint_start`） |

映射公式（反汇编确认）：
```
position=0   → joint_end（开）
position=100 → joint_start（关）
```

> VLA 抓取代码中 `claw_safe.py` 已统一按此映射，**不要参考旧版示例脚本或头文件注释**。

---

## 第 3 章：安全使用要点

### 3.1 力控保护

- 闭合时不要设到 `position=100`（蜗杆顶死），建议 `position=85-90`，留出安全余量
- 使用 `claw_safe.py` 封装的接口，不要直接调 `/control_robot_leju_claw` 服务

### 3.2 双爪协调

- Kuavo 两只手各有独立夹爪，默认同步控制
- `debug_left_claw.py` 可单独调试左手夹爪

### 3.3 配置路径

运行时读取的配置文件：
```
/home/lab/.config/lejuconfig/config.yaml
```
启动日志中可见 `[LEJU claw] config_path:...` 确认路径。

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **OpenClaw** | 行为树叶子节点，张开夹爪释放物体 |
| **CloseClaw** | 行为树叶子节点，闭合夹爪抓取物体 |
| **position** | 夹爪位置值（0=开，100=关，与部分文档相反） |
| **claw_safe.py** | VLA 夹爪安全封装脚本，统一位置映射 |
