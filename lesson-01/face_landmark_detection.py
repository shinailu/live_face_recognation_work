"""
使用dlib做人脸识别demo
"""

import dlib
from skimage import io

# 使用 Dlib 的正面人脸检测器 frontal_face_detector
detector = dlib.get_frontal_face_detector()

# Dlib 的 68点模型
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 图片所在路径
img = io.imread("1.jpg")

# 生成 Dlib 的图像窗口
win = dlib.image_window()
win.set_image(img)

# 使用 detector 检测器来检测图像中的人脸
faces = detector(img, 1)
print("人脸数：", len(faces))

for i, d in enumerate(faces):
    print("第", i+1, "个人脸的矩形框坐标：",
          "left:", d.left(), "right:", d.right(), "top:", d.top(), "bottom:", d.bottom())

    # 使用predictor来计算面部轮廓
    shape = predictor(img, faces[i])
    # 绘制面部轮廓
    win.add_overlay(shape)

# 绘制矩阵轮廓
win.add_overlay(faces)

# 保持图像
dlib.hit_enter_to_continue()