# 🌲 二叉树专题刷题执行清单

---
> **📌 文档定位：** 树专题清单 — 视频 + 15 道 LeetCode 分阶段执行计划
> **适合：** 已掌握 [DSA_C++_Basics](DSA_C++_Basics.md)，准备刷树相关 Hot 100
> **前置：** [四步破局法](data_stuctures_and_algorithms.md)（建议先读方法论）
> **后续：** [Job_Requirements](Job_Requirements_for_Robot.md) 阶段二（行为树思维衔接）
> **预计时间：** 1–2 周
> **🏠 返回总索引：** [README.md](README.md)

**外部资源：**
- 视频：[Bilibili 数据结构课程](https://space.bilibili.com/401399175/lists/3102780?type=season)
- 刷题：[LeetCode Hot 100](https://leetcode.cn/studyplan/top-100-liked/)

---

> 💡 **刷题方法：** 每道题建议用 [四步破局法](data_stuctures_and_algorithms.md) 拆解，不要直接背答案。

### 第一阶段：基础建树与初识递归（3道简单题）

这个阶段的目标是熟悉二叉树的底层长相，学会用递归去触碰树的每一个节点。

* **📺 核心必看视频：**
1. 《树（Tree）定义、术语、性质》
2. 《二叉树&完全二叉树-定义、性质》
3. 《二叉树的存储（顺序存储、链式存储）》
4. 《二叉树的遍历》（**先只看：前序、中序、后序遍历的递归实现**）


* **📝 对应冲刺题目：**
* **94. 二叉树的中序遍历（简单）** $\rightarrow$ *建议首题：套用网课递归模板。*
* **104. 二叉树的最大深度（简单）** $\rightarrow$ *体会怎么在递归回溯的时候，把高度一级级加自增上去。*
* **226. 翻转二叉树（简单）** $\rightarrow$ *大名鼎鼎的题，其实就是前序遍历，每到一个节点，把它的左右指针交换一下。*



---

### 第二阶段：层序遍历与广度优先（2道中等题）

本阶段涉及机器人在地图搜索里最常用的算法——**BFS（广度优先搜索）**。

* **📺 核心必看视频：**
* 继续看《二叉树的遍历》中的 **“层序遍历”** 部分（重点看它是怎么用队列（Queue）实现的）。


* **📝 对应冲刺题目：**
* **102. 二叉树的层序遍历（中等）** $\rightarrow$ *完美对应视频。机器人感知和路径规划的底座算法，必须练到盲打。*
* **199. 二叉树的右视图（中等）** $\rightarrow$ *层序遍历的变种，即每层取最右节点，其实就是层序遍历时，每一层只打印最后一个节点。*



---

### 第三阶段：二叉搜索树（BST）特性专题（3道题）

**注意：** 视频列表里没有单独列出“二叉搜索树”，但请死死记住它的**通关密码**：**“二叉搜索树的中序遍历结果，是一个严格升序的数组”**。

* **📺 核心必看视频：**
* 回看《二叉树的遍历》中 **“中序遍历”** 的特性。


* **📝 对应冲刺题目：**
* **98. 验证二叉搜索树（中等）** $\rightarrow$ *利用中序遍历，检查前一个节点是不是一直比后一个节点小。*
* **230. 二叉搜索树中第K小的元素（中等）** $\rightarrow$ *同样是中序遍历，走到第 K 个节点时直接返回答案。*
* **108. 将有序数组转换为二叉搜索树（简单）** $\rightarrow$ *用二分法的思想，每次找数组中间的值当根节点，两边递归建树。*



---

### 第四阶段：硬核结构变形与高阶递归（7道压轴题）

本阶段为树结构综合题。

* **📺 核心必看视频：**
* 《二叉树的构造 - 由遍历序列构造二叉树》


* **📝 对应冲刺题目：**
* **105. 从前序与中序遍历序列构造二叉树（中等）** $\rightarrow$ *完美对应刚刚看完的构造视频。*
* **101. 对称二叉树（简单）** $\rightarrow$ *双树同步递归，考察双指针同步递归。*
* **543. 二叉树的直径（简单）** $\rightarrow$ *虽然是简单题，但很精妙。在算深度的同时，顺便把左深度+右深度拼成直径。*
* **114. 二叉树展开为链表（中等）** $\rightarrow$ *考查指针的重定向，需要一点空间想象力。*
* **236. 二叉树的最近公共祖先（中等）** $\rightarrow$ *经典的后序遍历。自底向上回溯，找两个节点的交汇点。*
* **437. 路径总和 III（中等）** $\rightarrow$ *树上的双重递归，或者是树上结合前缀和，难度较高。*
* **124. 二叉树中的最大路径和（困难）** $\rightarrow$ *Hot 100 二叉树大 Boss。不要怕，它的本质和“二叉树直径”一模一样，只不过把计数变成了算节点分数的最大值。*



---

## 💡 助攻小贴士

Hot 100 中约 **80% 使用递归**。实现时**不必逐层模拟完整调用栈**，明确两件事即可：

1. **Base Case（什么时候停下来）：** 通常是 `if (root == nullptr) return ...;`
2. **单层逻辑（当前节点和左右儿子什么关系）：** 做好当前节点的事，剩下的放心抛给 `dfs(root->left)` 和 `dfs(root->right)`。

建议先完成第一阶段视频，再练习 LeetCode [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)。

---

## 📍 文档导航

| 方向 | 文档 |
| --- | --- |
| 🏠 总索引 | [README.md](README.md) |
| Python/C++ 分工 | [Python_C++_bridge.md](Python_C++_bridge.md) |
| Python 最小语法 | [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md) |
| 读 Python 源码 | [robotics_Python.md](robotics_Python.md) |
| 读 C++ 源码 | [robotics_C++.md](robotics_C++.md) |
| 刷题语法 (C++) | [DSA_C++_Basics.md](DSA_C++_Basics.md) |
| 写 C++ 代码 | [C++_grammar_supplement.md](C++_grammar_supplement.md) |
| 刷题方法论 | [data_stuctures_and_algorithms.md](data_stuctures_and_algorithms.md) |
| 树专题刷题 | [DSA_tree.md](DSA_tree.md) |
| 定方向 | [Job_Requirements_for_Robot.md](Job_Requirements_for_Robot.md) |
---

## 📍 文档导航

| 方向 | 文档 |
| --- | --- |
| 🏠 总索引 | [README.md](README.md) |
| Python/C++ 分工 | [Python_C++_bridge.md](Python_C++_bridge.md) |
| Python 最小语法 | [python/python_for_robotics_basics.md](python/python_for_robotics_basics.md) |
| 读 Python 源码 | [robotics_Python.md](robotics_Python.md) |
| 读 C++ 源码 | [robotics_C++.md](robotics_C++.md) |
| 刷题语法 (C++) | [DSA_C++_Basics.md](DSA_C++_Basics.md) |
| 写 C++ 代码 | [C++_grammar_supplement.md](C++_grammar_supplement.md) |
| 刷题方法论 | [data_stuctures_and_algorithms.md](data_stuctures_and_algorithms.md) |
| 树专题刷题 | [DSA_tree.md](DSA_tree.md) |
| 定方向 | [Job_Requirements_for_Robot.md](Job_Requirements_for_Robot.md) |
