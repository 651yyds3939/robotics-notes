# robotics-notes

[![机器人全链路系统 · 思维导图预览](./assets/robot_system_preview.png)](https://raw.githubusercontent.com/651yyds3939/robotics-notes/master/assets/robot_system_preview.png)

> **思维导图入口**：上图是**全展开**预览（含全部子节点）。**点击图片**可在新标签页打开高清原图并放大查看；源文件 [`robot_system.md`](./robot_system.md)。交互浏览：安装 [Markmap 扩展](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) 打开 md，或 clone 后用浏览器打开 [`robot_system_photo.html`](./robot_system_photo.html)。更新导图后运行 `./regenerate_robot_system_html.sh` 同步刷新预览图。

机器人**通用**知识库与 Ubuntu 开发环境笔记，与具体机型无关。 
侧重概念、架构、控制/感知/工程化链路；**不含**某一品牌人形机器人的魔改代码与真机排障。

人形机器人（Kuavo 4 Pro）二次开发实战见独立仓库 [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（与本文库为**两个 GitHub 仓库**，跨库链接请用 GitHub 地址，见下方「链接规范」）。

---

## 持续更新与本地同步

本仓库**会持续更新**（思维导图、专题笔记、工具链文档等）。若已通过 `git clone` 拉取到本机，日后想获取 GitHub 上的最新内容，在**该仓库根目录**执行：

```bash
cd /path/to/robotics-notes   # 改为本机实际路径
git pull
```

若本地有未提交修改，`git pull` 可能提示冲突；可先 `git stash` 暂存改动，同步后再 `git stash pop`，或先提交到 fork 再拉取。

**两库并排维护时**（例如 `~/Notes/robotics-notes` 与 `~/Notes/kuavo-dev-notes`），需分别在两个目录各执行一次 `git pull`。通用笔记在本仓库；Kuavo 实战在 [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)。

**首次克隆本仓库：**

```bash
git clone https://github.com/651yyds3939/robotics-notes.git
cd robotics-notes
```


---

## 这个仓库怎么用

### 推荐阅读顺序

1. **先看思维导图** [`robot_system.md`](./robot_system.md) — 建立「感知 → 决策 → 控制 → 执行 → 通信 → 工程化」全链路地图；节点上的链接可跳到本仓库专题笔记，或 [`kuavo-dev-notes`](https://github.com/651yyds3939/kuavo-dev-notes) 里的对应实战文档。
2. **按链路查专题** — 在 [`robotics/`](./robotics/) 里找 ROS、SLAM、RL、动力学、Docker 等深度笔记。
3. **环境/工具踩坑** — 在 [`ubuntu/`](./ubuntu/) 里查 Conda、Cursor、代理、磁盘清理等。
4. **要写代码时** — 用 [`robotics/ros_code_template/`](./robotics/ros_code_template/) 里的 ROS1/ROS2 模板；C++ 基础见 [`robotics/code/`](./robotics/code/)。

### 与 kuavo-dev-notes 的分工

| 仓库 | 定位 |
|------|------|
| **robotics-notes**（本仓库） | 通用理论、架构、工具链；思维导图串联知识点 |
| **kuavo-dev-notes** | Kuavo 4 Pro 实机/仿真二次开发：终端命令、魔改代码、54 篇实战 `.md` |

思维导图里的「👉 实战案例」链接多数指向 kuavo-dev-notes；「👉 专题笔记」链接指向本仓库 `robotics/` 或 `ubuntu/`。

---

## 链接规范（两仓库分工）

`robotics-notes` 与 [`kuavo-dev-notes`](https://github.com/651yyds3939/kuavo-dev-notes) 是**两个独立 GitHub 仓库**。Markdown 链接按目标分三种写法：

| 跳转目标 | 推荐写法 | 说明 |
|----------|----------|------|
| **本仓库内**（`robotics/`、`ubuntu/`、`robot_system.md`） | 相对路径 | 例：`[RL 笔记](./robotics/RL.md)` — 在 GitHub 与本机克隆内均可点击 |
| **kuavo 实战文档**（`kuavo_notes/*.md`） | **GitHub 绝对链接** | 例：`https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/15.4RL_lab_sim_to_real.md` |
| **本地 Notes 并排目录**（可选） | 仅自用，不写进要 push 的文档 | 本机 `~/Notes/kuavo-dev-notes` 可用 IDE 打开，但 GitHub 上 `../kuavo-dev-notes` **无效** |

思维导图 [`robot_system.md`](./robot_system.md) 中：

- **👉 专题笔记** → 本仓库相对路径（通用理论）
- **👉 实战案例** → kuavo 仓库 GitHub 链接（Kuavo 真机/魔改）

维护跨库链接时，可复用下列前缀（`master` 换成仓库实际默认分支即可）：

```text
# kuavo 实战文档
https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/<文件名>.md

# 本仓库专题（若需在 kuavo 侧引用 robotics 通用笔记）
https://github.com/651yyds3939/robotics-notes/blob/master/robotics/<文件名>.md
```

---

## 思维导图：robot_system.md

[`robot_system.md`](./robot_system.md) 是**机器人全链路系统**的主索引，按九大层组织：

| 层级 | 内容概要 |
|------|----------|
| 一、感知层 | 传感器、视觉/语音、状态估计、标定 |
| 二、决策层 | ROS 中间件、SLAM/导航、机械臂规划、VLA/大模型 |
| 三、控制层 | PID、WBC/MPC、阻抗控制、RL / 世界模型 |
| 四、执行层 | FOC 电机、关节/末端执行器 |
| 五、机械结构层 | URDF/MJCF、底盘形态 |
| 六、安全 | 急停、限位、真机 SOP |
| 七、通信 | ROS 话题/服务、上下位机、TF |
| 八、电源 | 电池与配电（提纲） |
| 九、工程化 | 仿真、Sim2Real、Docker、Git、AI 辅助开发 |

导图内已加入大量**可点击跳转链接**（本仓库专题 + kuavo-dev-notes 实战案例）。除 Markmap 外，也可在编辑器中打开该文件，用大纲视图（`Ctrl+Shift+O`）浏览树状结构。

### 用 Markmap 查看（推荐）

1. 在 VS Code / Cursor 中安装扩展：**Markmap**（搜索 `markmap` 或 `Markmap for VS Code`）。
2. 打开 [`robot_system.md`](./robot_system.md)。
3. 在编辑区**右键** → 选择 **「Open in Markmap」**（或「在 Markmap 中打开」）。
4. 即可查看详细思维导图，并点击链接跳转。

### 用浏览器打开 HTML 版（离线）

[`robot_system_photo.html`](./robot_system_photo.html) 是思维导图的**离线快照**：数据已预渲染进 HTML，依赖本仓库 `assets/markmap/`，**无需联网**。更新 `robot_system.md` 后需重新生成本文件，内容可能略滞后于 `.md`。

**打开方式（任选其一）：**

1. **文件管理器** — 进入本仓库目录，双击 `robot_system_photo.html`。
2. **终端**（推荐，路径最不容易错）：
 ```bash
 xdg-open /home/lwy/Notes/robotics-notes/robot_system_photo.html # 将 lwy 与路径改为本机实际用户名与目录
 ```
 指定浏览器示例（路径同上，按需选用）：

 Google Chrome：
 ```bash
 google-chrome /home/lwy/Notes/robotics-notes/robot_system_photo.html # 将 lwy 与路径改为本机实际用户名与目录
 ```

 Firefox：
 ```bash
 firefox /home/lwy/Notes/robotics-notes/robot_system_photo.html # 将 lwy 与路径改为本机实际用户名与目录
 ```
3. **Cursor / VS Code** — 在文件树中右键 `robot_system_photo.html` → **Reveal in File Explorer**（或 **Open with… → 系统默认浏览器**）。
4. **浏览器内** — `Ctrl + O`，选择上述路径下的 `robot_system_photo.html`。

**注意：**

- 请从 **`robotics-notes/` 目录内**打开该 HTML（或保持 `assets/markmap/` 相对路径有效）；单独拷贝 HTML 到其他位置会导致脚本加载失败。
- 若主区域空白、仅见右下角 Markmap 工具栏：点工具栏中的 **「适应屏幕」**（四角方框图标），或 `Ctrl + Shift + R` 强制刷新。
- 需要与 `robot_system.md` 完全同步时，仍推荐上一节的 **Markmap 扩展** 直接打开 `.md`。

---

## 目录结构

```text
robotics-notes/
├── README.md                      # 本文件
├── robot_system.md                # 全链路思维导图（主入口，含跳转链接）
├── robot_system_photo.html        # 思维导图 HTML 快照
├── robotics/                      # 机器人通用专题（32 篇 .md）
│   ├── robotics_architecture_master_guide.md   # 架构总览（含 Docker 实战）
│   ├── robot_types.md             # 机器人形态对比
│   ├── ros_*.md, tf_tree.md       # ROS 通信 / 架构 / ROS2 流程
│   ├── slam.md, path_planning.md  # 导航与规划
│   ├── dynamics_control.md, pid_control.md, impedance_control.md
│   ├── RL.md, world_model.md      # 强化学习与世界模型
│   ├── motor_foc.md, robot_modeling.md, ...
│   ├── code/                      # C++ / DSA 编程基础
│   └── ros_code_template/         # ROS1 / ROS2 最小工作空间模板
└── ubuntu/                        # Ubuntu 开发与运维（21 篇 .md）
    ├── conda.md, cursor.md, Terminal_tools.md
    ├── claude_code_deepseek.md, AI_Coding_Agent.md
    └── 网络代理、磁盘清理、Boot 优化等
```

---

## robotics/ 专题索引（按主题）

| 主题 | 文档 |
|------|------|
| 总览与架构 | [`robotics_architecture_master_guide.md`](./robotics/robotics_architecture_master_guide.md) · [`robot_system_integration.md`](./robotics/robot_system_integration.md) · [`robot_types.md`](./robotics/robot_types.md) |
| ROS | [`ros_communication.md`](./robotics/ros_communication.md) · [`ros_logic.md`](./robotics/ros_logic.md) · [`ros2_process.md`](./robotics/ros2_process.md) · [`tf_tree.md`](./robotics/tf_tree.md) |
| 感知与定位 | [`camera_calibration.md`](./robotics/camera_calibration.md) · [`state_estimation.md`](./robotics/state_estimation.md) · [`sensor_fusion.md`](./robotics/sensor_fusion.md) · [`slam.md`](./robotics/slam.md) · [`AI_learning_robotics.md`](./robotics/AI_learning_robotics.md) |
| 规划与控制 | [`path_planning.md`](./robotics/path_planning.md) · [`pid_control.md`](./robotics/pid_control.md) · [`dynamics_control.md`](./robotics/dynamics_control.md) · [`impedance_control.md`](./robotics/impedance_control.md) · [`optimization_theory.md`](./robotics/optimization_theory.md) |
| 学习与部署 | [`RL.md`](./robotics/RL.md) · [`world_model.md`](./robotics/world_model.md) · [`edge_deployment.md`](./robotics/edge_deployment.md) |
| 建模与执行 | [`robot_modeling.md`](./robotics/robot_modeling.md) · [`motor_foc.md`](./robotics/motor_foc.md) |
| 工程化 | [`environment.md`](./robotics/environment.md) · [`docker.md`](./robotics/docker.md) · [`git_github.md`](./robotics/git_github.md) · [`git_pull.md`](./robotics/git_pull.md) · [`linux_C++_project.md`](./robotics/linux_C++_project.md) · [`terminal_command.md`](./robotics/terminal_command.md) · [`tools.md`](./robotics/tools.md) |
| 阅读与文档 | [`code_read_skill.md`](./robotics/code_read_skill.md) · [`doc_concept.md`](./robotics/doc_concept.md)（工作空间文件速查） · [`doc_function.md`](./robotics/doc_function.md)（动手学 ROS2 索引，建设中） |

编程基础与模板：[`robotics/code/`](./robotics/code/) · [`robotics/ros_code_template/`](./robotics/ros_code_template/)

---

## ubuntu/ 常用入口

按需查阅，无固定阅读顺序。常见入口：

- 开发环境：[`conda.md`](./ubuntu/conda.md) · [`download.md`](./ubuntu/download.md) · [`clear_space.md`](./ubuntu/clear_space.md)
- IDE / AI：[`cursor.md`](./ubuntu/cursor.md) · [`claude_code_deepseek.md`](./ubuntu/claude_code_deepseek.md) · [`AI_Coding_Agent.md`](./ubuntu/AI_Coding_Agent.md) · [`AI_sort_out_notes.md`](./ubuntu/AI_sort_out_notes.md)
- 终端与工具：[`Terminal_tools.md`](./ubuntu/Terminal_tools.md) · [`tools.md`](./ubuntu/tools.md) · [`cd.md`](./ubuntu/cd.md)
- 网络：[`airport_vpn.md`](./ubuntu/airport_vpn.md) · [`auto_clash.md`](./ubuntu/auto_clash.md) · [`arm_clash.md`](./ubuntu/arm_clash.md)

---

## 快速链接

| 用途 | 链接 |
|------|------|
| 思维导图（Markmap） | [`robot_system.md`](./robot_system.md) |
| 思维导图（浏览器离线 HTML） | [`robot_system_photo.html`](./robot_system_photo.html) |
| 架构长文 | [`robotics/robotics_architecture_master_guide.md`](./robotics/robotics_architecture_master_guide.md) |
| Kuavo 实战仓库 | [kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes) |

---

*本仓库为个人学习整理，通用知识以最新专题笔记为准；与官方文档冲突时请以厂商文档为准。*
