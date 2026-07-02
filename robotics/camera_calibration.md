# 相机模型与标定 (Camera Model & Calibration)

> **核心定位**：相机是机器人最重要的外部传感器——但相机看到的是**像素坐标** $(u, v)$，机器人需要的是**世界坐标** $(X, Y, Z)$。相机模型是这两个坐标系之间的数学桥梁。标定就是求这座桥的参数。
>
> 👉 相关：[TF 树](./tf_tree.md) · [AI 与机器人学习](./AI_learning_robotics.md)
> 👉 实战笔记：[YOLO + TF2 坐标变换抓取](https://github.com/651yyds3939/kuavo-dev-notes/blob/master/kuavo_notes/4.4real_visual_grasp.md)

---

## 第 0 章：相机标定一句话

> **大白话**：相机拍出来的照片是"变形的"（广角镜头的桶形畸变）。标定用于确定「像素点在相机/世界坐标系中的方向」。标定完了，YOLO 检测到的像素框才能转化成机器人坐标系下的抓取目标点。

---

## 第 1 章：针孔相机模型 (Pinhole Model)

### 1.1 从世界坐标到像素坐标——四步变换

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \cdot \begin{bmatrix} R \mid t \end{bmatrix} \cdot \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}$$

| 步 | 矩阵 | 含义 |
|----|------|------|
| 1 | $[R \mid t]$ | **外参**：世界坐标系 → 相机坐标系（旋转+平移） |
| 2 | $K$ | **内参**：相机坐标系 → 像素坐标系 |
| 3 | $\lambda$ | 深度缩放因子 |

### 1.2 内参矩阵 $K$

$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

- $f_x, f_y$：焦距（像素单位），$f_x = f / p_x$（物理焦距 ÷ 像素宽度）
- $c_x, c_y$：主点（光轴与图像平面的交点，通常接近图像中心）
- 对于 RealSense D435i：$f_x \approx 610$, $c_x \approx 320$ (640×480 分辨率)

---

## 第 2 章：畸变模型

> 广角镜头的图像边缘会"弯"。标定需要建模并矫正这种畸变。

### 径向畸变 (Radial Distortion)

$$\begin{aligned} x_{distorted} &= x(1 + k_1 r^2 + k_2 r^4 + k_3 r^6) \\ y_{distorted} &= y(1 + k_1 r^2 + k_2 r^4 + k_3 r^6) \end{aligned}$$

### 切向畸变 (Tangential Distortion)

$$\begin{aligned} x_{distorted} &= x + [2p_1 xy + p_2(r^2 + 2x^2)] \\ y_{distorted} &= y + [p_1(r^2 + 2y^2) + 2p_2 xy] \end{aligned}$$

> 其中 $r^2 = x^2 + y^2$，$(x, y)$ 是归一化的无畸变坐标。OpenCV 用 5 参数向量 $[k_1, k_2, p_1, p_2, k_3]$ 描述。

---

## 第 3 章：张正友标定法 (Zhang's Method)

用棋盘格（已知方格尺寸）从多个角度拍照，求解内参和畸变：

```python
import cv2
import numpy as np

# 准备棋盘格（如 9×6 内角点，格子 25mm）
pattern_size = (9, 6)
square_size = 0.025 # 米

# 检测角点并标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
 objpoints, # 棋盘格角点的世界 3D 坐标
 imgpoints, # 检测到的图像 2D 角点
 image_size, # 图像分辨率
 None, None
)

# 矫正图像
new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, image_size, 1)
undistorted = cv2.undistort(img, mtx, dist, None, new_mtx)
```

---

## 第 4 章：手眼标定 (Hand-Eye Calibration)

> 相机装在机器人**手臂上**（eye-in-hand）或**固定位置看手**（eye-to-hand）。手眼标定求的是**相机相对于机器人末端/基座的固定变换矩阵**。

### 核心方程（eye-in-hand）

$$AX = XB$$

- $A$：机器人末端的运动（已知，从正运动学得到）
- $B$：相机视野中标定板的运动（已知，从相机外参得到）
- $X$：**待求**的相机→末端固定变换

> 解 $AX = XB$ 需要至少 2 组非共轴的运动，常用 Tsai-Lenz 方法。

---

## 关键词速查

| 术语 | 解释 |
|------|------|
| **内参 $K$** | 焦距 + 主点，描述相机光学特性 |
| **外参 $[R \mid t]$** | 相机坐标系在世界/基座坐标系中的位姿 |
| **畸变参数** | $[k_1, k_2, p_1, p_2, k_3]$ 描述镜头畸变 |
| **张正友标定** | 用棋盘格多角度拍照求解内参+畸变 |
| **手眼标定** | 求相机与机器人末端/基座的固定变换 $X$ |
