# ROS / Ubuntu 工作空间文件速查（各类型文件是干什么的）

> **核心定位**：刚打开一个 ROS 工作空间，满屏 `CMakeLists.txt`、`package.xml`、`setup.py` 容易懵。本篇按**目录层级 → 文件后缀/类型**说明「这是啥、谁生成、能不能改、删了会怎样」。
>
> 👉 配套：[ROS2 开发流程](./ros2_process.md) · [ROS 架构逻辑](./ros_logic.md) · [代码模板](./ros_code_template/ros2_code_ws/) · [动手学 ROS2 教程索引](./doc_function.md)

---

## 一、工作空间（Workspace）顶层目录

典型路径：`~/ros2_ws` 或 `~/catkin_ws`（部分厂商官方包常见 `~/kuavo-ros-opensource` 等）。

| 路径 / 文件 | ROS 1 (catkin) | ROS 2 (colcon) | 作用 |
|-------------|----------------|----------------|------|
| **`src/`** | ✅ 必有 | ✅ 必有 | **源码区**：功能包、克隆的第三方包、子模块都在这。**唯一应长期维护的目录**。 |
| **`build/`** | ✅ | ✅ | **编译中间产物**：`.o`、CMake 缓存、`CMakeCache.txt`。可 `rm -rf build` 后重编。 |
| **`devel/`** | ✅ | ❌（ROS2 无 devel） | **开发 overlay**：`source devel/setup.bash` 后当前终端能 `rosrun/roslaunch`。ROS2 用 `install/` 代替。 |
| **`install/`** | 可选 | ✅ 默认 | **安装前缀**：`colcon build` 把可执行文件、launch、msg 装到这里；`source install/setup.bash` 生效。 |
| **`log/`** | 较少 | ✅ | **colcon 编译日志**：某包编译失败时先看 `log/latest/`。 |
| **`.catkin_workspace`** | ✅ 空标记文件 | — | 告诉 catkin「这是工作空间根目录」。 |
| **`COLCON_IGNORE`** | 可放子目录 | ✅ | 放某目录下表示 **colcon 跳过该目录**（不编译）。 |

**记忆口诀**：只改 `src/`；`build/`、`devel/`、`install/`、`log/` 都是**可再生**的。

---

## 二、功能包（Package）必备与常见文件

每个包是 `src/` 下的一个子目录，例如 `src/my_robot_bringup/`。

### 2.1 包「身份证」（必看）

| 文件 | 作用 | 维护说明 |
|------|------|------------|
| **`package.xml`** | 包的**元数据**：名字、版本、作者、**依赖列表**（`depend`/`build_depend`/`exec_depend`）。ROS 工具靠它解析依赖图。 | 加新依赖（如 `rclcpp`、`sensor_msgs`）必须改这里。 |
| **`CMakeLists.txt`** | **C++ 包的组装说明书**：找源文件、链库、生成可执行节点、安装 launch/config。ament_cmake 包的核心。 | 新增 `.cpp` 节点、msg、库时改这里。不是可执行程序本身。 |
| **`setup.py`** | **Python 包入口**（`ament_python`）：声明包名、依赖、`console_scripts`（把命令名映射到 `模块:函数`）。 | 新增 Python 节点时改 `entry_points`。 |
| **`setup.cfg`** | Python 包安装细节（如 pytest、flake8 路径），常由 `ros2 pkg create` 生成。 | 一般少改。 |
| **`resource/<包名>`** | ROS2 Python 包的**空标记文件**，让 ament 识别包资源。 | 自动生成，勿删。 |

### 2.2 源码与节点

| 类型 | 常见路径 | 作用 |
|------|----------|------|
| **`.cpp` / `.hpp`** | `src/`、`include/<包名>/` | C++ 节点与算法实现；编译成 `install/lib/<包名>/` 下的可执行文件。 |
| **`.py`** | `<包名>/<包名>/xxx.py` | Python 节点；通过 `setup.py` 的 `console_scripts` 注册为命令。 |
| **`__init__.py`** | Python 包目录内 | 标记 Python 模块目录。 |

### 2.3 接口定义（消息 / 服务 / 动作）

| 后缀 | 作用 | 生成物 |
|------|------|--------|
| **`.msg`** | **话题消息**结构（如 `JointState`、`Image`）。 | 编译成 C++/Python 的 `xxx.msg` 类，供 publish/subscribe。 |
| **`.srv`** | **服务**请求+响应（一问一答）。 | 生成 `xxx.srv` 的 Request/Response 类。 |
| **`.action`** | **长任务**（带反馈，如导航到点）。 | 生成 Action 客户端/服务端类型（ROS2 常用）。 |

自定义接口通常放在包内 `msg/`、`srv/`、`action/`，并在 `CMakeLists.txt` 里 `rosidl_generate_interfaces`。

---

## 三、Launch、参数与运行时配置

| 类型 | 示例 | 作用 |
|------|------|------|
| **`.launch`（XML）** | ROS1 | 一次启动多个节点、传参、remap 话题名。 |
| **`.launch.py`** | ROS2 | Python 写 launch，更灵活（条件启动、仿真/实机分支）。 |
| **`.yaml` / `.yml`** | `config/params.yaml` | **参数文件**：PID 增益、话题名、算法超参；由 launch 加载到 Parameter Server。 |
| **`.json`** | 部分驱动 / Foxglove | 结构化配置或可视化布局导出。 |
| **`.xml`** | `plugin.xml`、部分 legacy 配置 | 插件描述、驱动 manifest 等。 |

**Launch 不负责算路**，只负责「把计算图搭起来」——详见 [ROS 架构逻辑](./ros_logic.md)。

---

## 四、机器人模型、仿真与世界文件

| 类型 | 作用 | 关联 |
|------|------|------|
| **`.urdf`** | 连杆、关节、惯量、碰撞体的**静态机器人描述**。 | [机器人建模](./robot_modeling.md) |
| **`.xacro`** | URDF 的**宏模板**（复用、传参），编译成 URDF 再给 RViz/MoveIt。 | 人形/机械臂几乎都用 xacro 维护。 |
| **`.srdf`** | MoveIt **语义描述**：规划组、禁碰对、默认姿态。 | 运动规划必备。 |
| **`.sdf` / `.world`** | Gazebo / Ignition **仿真世界**与模型。 | 仿真环境 |
| **`.dae` / `.stl` / `.obj`** | 网格 **mesh**（外观或碰撞）。 | `meshes/` 目录 |
| **`.rviz`** | RViz **可视化布局**（显示哪些 TF、点云、Marker）。 | 调试常用 |

---

## 五、控制、导航与 TF 相关

| 类型 / 名 | 作用 |
|-----------|------|
| **`ros2_control` / `transmission` YAML** | 声明硬件接口、关节、控制器类型（位置/力矩）。 |
| **`costmap_*.yaml`** | 导航代价地图参数（膨胀半径、障碍物层）。 |
| **`moveit_*`** | MoveIt 规划场景、 kinematics、OMPL 配置。 |
| **TF 树** | 无单独后缀；由 `robot_state_publisher` + URDF + 定位节点发布。见 [TF 树笔记](./tf_tree.md)。 |

---

## 六、编译产物与「能不能删」

| 产物 | 位置 | 说明 |
|------|------|------|
| **可执行节点** | `install/lib/<包名>/` 或 `devel/lib/` | `ros2 run pkg node` 运行的二进制。 |
| **共享库 `.so`** | `install/lib/` | 插件、算法库。 |
| **生成的 msg 头文件** | `build/`、`install/include/` | 由 `.msg/.srv` 自动生成，勿手改。 |
| **`setup.bash` / `local_setup.bash`** | `install/`、`devel/` | **环境脚本**：把本工作空间 overlay 到 ROS 系统路径。 |
| **`.ament_index/`** | `install/` | ROS2 包索引，供 `ros2 pkg list` 发现包。 |

---

## 七、数据录制、模型与部署（工作空间周边）

| 类型 | 作用 |
|------|------|
| **`.bag`（ROS1）** | 录制的 topic 快照，离线回放调试。 |
| **`.db3` / `.mcap`（ROS2）** | 同上；MCAP 带索引，大文件打开更快。 |
| **`.onnx` / `.pt` / `.engine`** | 训练策略或感知模型；部署见 [边缘模型部署](./edge_deployment.md)。 |
| **`.info` / `.yaml`（RL 配置）** | 人形 RL 控制器观测维度、关节顺序等（Sim2Real 对齐关键）。 |

---

## 八、Ubuntu / 工程化常见文件（非 ROS 专属）

| 文件 | 作用 |
|------|------|
| **`Dockerfile` / `docker-compose.yml`** | 容器化运行环境。见 [Docker 笔记](./docker.md)。 |
| **`.gitignore`** | 忽略 `build/`、`install/`、`log/`、大 bag，避免误 commit。 |
| **`README.md`** | 包/仓库说明。 |
| **`.vscode/`、`c_cpp_properties.json`** | IDE 头文件路径、clangd；模板见 [ros_code_template](./ros_code_template/ros2_code_ws/.vscode/)。 |
| **`requirements.txt` / `environment.yml`** | Python 非 ROS 依赖（PyTorch 等）；与 Conda 见 [环境笔记](./environment.md)。 |
| **`Makefile` / `scripts/*.sh`** | 一键编译、部署、真机启动脚本。 |

---

## 九、ROS 1 vs ROS 2 对照（只看文件差异）

| 概念 | ROS 1 | ROS 2 |
|------|-------|-------|
| 编译 | `catkin_make` / `catkin build` | `colcon build` |
| 环境 | `source devel/setup.bash` | `source install/setup.bash` |
| 运行 | `rosrun` / `roslaunch` | `ros2 run` / `ros2 launch` |
| Python 包 | `catkin` + `setup.py` 混用 | `ament_python` + `setup.py` 规范 |
| Launch | `.launch` (XML) | `.launch.py` (Python) 为主 |
| 参数 | `rosparam` | `ros2 param` + YAML |

---

## 十、阅读顺序建议

1. 打开 **`package.xml`** → 知道包叫什么、依赖谁。 
2. 看 **`CMakeLists.txt` 或 `setup.py`** → 知道有哪些节点、装哪些文件。 
3. 看 **`launch/`** → 知道运行时启动了谁。 
4. 看 **`config/*.yaml`** → 知道参数从哪来。 
5. 再进 **`src/`** 读算法——配合 [代码阅读技巧](./code_read_skill.md)。

---

## 十一、与实战案例仓库的关系

Kuavo 官方/魔改仓库里还会出现：`humanoid_controllers`、EtherCAT 配置、`.info` RL 参数等——属于**项目专有扩展**，通用结构仍符合上表。真机排障案例见 GitHub：[kuavo-dev-notes](https://github.com/651yyds3939/kuavo-dev-notes)（跨库链接请用 GitHub 地址，见 [README 链接规范](../README.md#链接规范两仓库分工)）。
