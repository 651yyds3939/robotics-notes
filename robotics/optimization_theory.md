# 优化理论在机器人中的应用 (Optimization for Robotics)

> **核心定位**：优化理论是现代机器人控制算法的数学底座。WBC 在求解 QP、MPC 在求解有限时域最优控制、IK 在做非线性最小二乘、轨迹规划在做约束优化——几乎所有"高级控制"问题最终都归结为一个优化问题。理解优化，你就理解了"为什么这些算法能动"。

---

## 第 0 章：优化理论一句话

> **大白话**：机器人做任何事都可以变成一个问题——"在满足 XX 约束的前提下，找到让某个指标最好的那个动作"。优化理论就是解这类问题的数学工具箱。WBC 解"怎么分配力矩让机器人最稳"，MPC 解"接下来几步怎么走最省力"，IK 解"怎么转关节让手到那个位置"。

---

## 第 1 章：优化问题的标准形式

$$\begin{aligned} \min_x \quad & f(x) && \text{(目标函数/代价)} \\ \text{s.t.} \quad & g_i(x) \leq 0 && \text{(不等式约束)} \\ & h_j(x) = 0 && \text{(等式约束)} \end{aligned}$$

### 常见分类

| 类型 | $f(x)$ | 约束 | 机器人中的应用 |
|------|--------|------|--------------|
| **线性规划 (LP)** | 线性 | 线性 | 简单资源分配 |
| **二次规划 (QP)** | 二次型 | 线性 | **WBC**、MPC 的每一步 |
| **非线性规划 (NLP)** | 非线性 | 非线性 | 轨迹优化、IK（非冗余） |
| **最小二乘** | $\|r(x)\|^2$ | 无/有 | **[SLAM 后端](./slam.md)**、BA、[IK](./dynamics_control.md) |

---

## 第 2 章：二次规划 (QP) —— WBC 的核心引擎

全身控制 (WBC) 在 1kHz 频率下，每一步都在求解一个 QP：

$$\begin{aligned} \min_{\ddot{q}, \tau, F} \quad & \|A\ddot{q} - b\|^2 + \|\tau\|^2 \\ \text{s.t.} \quad & \tau = M(q)\ddot{q} + C(q,\dot{q}) + G(q) - J_c^T F \\ & F \in \text{Friction Cone} \\ & \tau_{\min} \leq \tau \leq \tau_{\max} \\ & \ddot{q}_{\min} \leq \ddot{q} \leq \ddot{q}_{\max} \end{aligned}$$

> **凭什么 1kHz 能解 QP？** QP 有解析条件（KKT），而且线性约束 + 凸目标 = 全局最优，求解器（如 qpOASES / OSQP / HPIPM）做了极致优化，能在微秒级解出。

---

## 第 3 章：非线性优化与 KKT 条件

对于无约束非线性问题，极值点满足 $\nabla f(x^*) = 0$。对于有约束问题，**KKT 条件**（Karush-Kuhn-Tucker）是判断最优解的一阶必要条件：

$$\begin{aligned} \nabla f(x^*) + \sum \lambda_i \nabla g_i(x^*) + \sum \mu_j \nabla h_j(x^*) &= 0 \\ g_i(x^*) &\leq 0 \\ h_j(x^*) &= 0 \\ \lambda_i &\geq 0 \\ \lambda_i g_i(x^*) &= 0 \quad \text{(互补松弛：要么约束生效，要么 λ 为 0)} \end{aligned}$$

> **Lagrange 乘子 $\lambda$** 直观含义：打破约束的"代价"。$\lambda_i$ 越大 = 这个约束对最优解的限制越强。

---

## 第 4 章：机器人中的优化应用速查

| 算法 | 优化类型 | 频率 | 求解器 |
|------|---------|------|--------|
| **WBC** | QP | 1kHz | qpOASES / OSQP / HPIPM |
| **MPC** | QP / NLP (滚动时域) | 50-200Hz | 同上 + IPOPT / SNOPT |
| **IK (冗余机械臂)** | QP (关节速度最小范数) | 100-500Hz | OSQP / 手写解析解 |
| **SLAM 后端** | 非线性最小二乘 + 稀疏 | ~1Hz (关键帧) | Ceres / g2o / GTSAM |
| **轨迹优化** | NLP (多 shooting / collocation) | 离线或低频 | IPOPT / SNOPT / CasADi |
| **[MPPI (TD-MPC2)](./world_model.md)** | 无梯度的采样优化 | 50Hz | 纯采样，不需要求解器 |

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **QP** | 二次规划：目标二次型 + 线性约束，WBC/MPC 的数学形式 |
| **KKT 条件** | 约束优化的一阶必要条件，拉格朗日乘子法的推广 |
| **Lagrange Multiplier $\lambda$** | 打破约束的"影子价格" |
| **Convex vs Non-convex** | 凸问题 = 局部最优 = 全局最优，非凸问题可能有多解 |
| **Complementary Slackness** | 互补松弛：$\lambda_i g_i(x^*) = 0$，要么约束生效要么乘子为零 |
| **Active Set** | 当前起作用的约束集合，QP 求解器常用的方法 |
