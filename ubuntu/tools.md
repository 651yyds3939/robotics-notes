
## 1. 终端与效率增强 (Terminal & Shell)

以下工具可提升终端与开发体验：

* **Starship**: 跨 shell 提示符，可显示 Conda 环境、Git 分支、ROS 变量等。
* **Zellij**: 终端复用器。同时运行 `roscore`、`gazebo` 与训练脚本时，布局管理与浮动窗口便于并行调试。
* **LazyGit**: 一个非常丝滑的终端 Git 图形界面。若嫌 `git status`、`add`、`commit` 繁琐，LazyGit 可通过快捷键完成所有操作，视觉化效果极佳。

---

## 2. 机器人开发专属 (Robotics Specific)

人形机器人与 RL 相关，这几个工具是行业标配：

* **Foxglove Studio**: 可以看作是增强版的 Rviz。它支持现代化的 UI 布局，可以通过 Web 或客户端连接到 ROS1/ROS2 节点。它的调试曲线图和 3D 可视化比原生的 Rviz 漂亮且强大得多，非常适合分析传感器数据。
* **PlotJuggler**: 机器人开发者的必备。若需实时或回放分析 `.bag` 数据流，它的时序图分析功能极其强大，可以轻松进行数学运算和数据对比。

---

## 3. 知识管理与科研准备 (Knowledge & Academic)

技术文档与论文整理、算法推导和未来的学术研究：

* **Obsidian**: 一个基于本地 Markdown 文件的知识库工具。适合记录 RL 调参、机器人架构图等 Markdown 笔记；与 Git 配合良好，也可直接编写项目 README。
* **Zotero**: 文献管理的神。阅读 RL/机器人顶会论文时或机器人领域的顶会论文（如 ICRA, IROS, CoRL），Zotero 的插件（如 ZotFile 和翻译插件）可批量整理文献，并自动提取笔记。

---

## 4. AI 搜索与信息检索

* **Perplexity AI**: 当需要查找某个具体的库函数用法，或者调研某个特定的历史文化背景、古建筑结构时，Perplexity 比传统的 Google 搜索更高效。可汇总答案并附参考来源并列出所有参考来源，非常适合技术调研。

---

## 5. 视觉资产管理 (Visual Assets)

* **Eagle**: 若需整理大量参考图库、博物馆照片或古建筑参考图，Eagle 是目前整理图片最好的工具之一。它支持标签、文件夹、颜色搜索，便于按标签/文件夹整理大量素材。

---

### 💡 一个小建议

工具不在多，而在于**能不能串成一套闭环**。

典型链路：**Perplexity** 调研 $\rightarrow$ **Cursor** 编码 $\rightarrow$ **Foxglove** 调试 $\rightarrow$ **Obsidian** 记录参数与逻辑。

