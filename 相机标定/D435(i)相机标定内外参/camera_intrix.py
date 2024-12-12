import cv2
import numpy as np
import glob
import yaml


# numpy不使用科学计数法
np.set_printoptions(suppress=True)
# 控制输出的精度（小数点后面的位数是10位）
np.set_printoptions(precision=10,suppress=True)

# 找棋盘格角点
# 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # 阈值
# 棋盘格模板规格
w = 11  # 10 - 1
h = 8  # 7  - 1
# 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
objp = np.zeros((w * h, 3), np.float32)
objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
objp = objp * 25  #  注意改参数！！！！！棋盘格的每格的长度！

# 储存棋盘格角点的世界坐标和图像坐标对
objpoints = []  # 在世界坐标系中的三维点
imgpoints = []  # 在图像平面的二维点

# 加载chess文件夹下的所有的jpg图像
images = glob.glob('./chess/*.png')  # 拍摄的十几张棋盘图片所在目录

i = 0
for fname in images:

    img = cv2.imread(fname)
    # 获取画面中心点
    # 获取图像的长宽
    h1, w1 = img.shape[0], img.shape[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    u, v = img.shape[:2]
    # 找到棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
    # 如果找到足够点对，将其存储起来
    if ret == True:
        print("i:", i)
        i = i + 1
        # 在原角点的基础上寻找亚像素角点
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # 追加进入世界三维点和平面二维点中
        objpoints.append(objp)
        imgpoints.append(corners)
        # 将角点在图像上显示
        cv2.drawChessboardCorners(img, (w, h), corners, ret)
        cv2.namedWindow('findCorners', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('findCorners', 1280, 720)
        cv2.imshow('findCorners', img)
        cv2.waitKey()
cv2.destroyAllWindows()
# %% 标定
print('正在计算')
print(u, v)
# 标定
ret, mtx, dist, rvecs, tvecs = \
    cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# 写入文件
###写入文件路径###
file_path = ("./标定文件.yaml")
###写入文件路径###

# 存取标定数据
mtx_yaml = mtx.tolist()
dist_yaml = dist.tolist()
camera_u, camera_v = u, v
data = {"information": "Camera calibration parameters", "camera_matrix": mtx_yaml, "dist_coeff": dist_yaml,
        "camera_u": camera_u, "camera_v": camera_v}
with open(file_path, "w") as file:
    yaml.dump(data, file)

print("ret:", ret)
print("mtx:\n", mtx)  # 内参数矩阵
print("dist畸变值:\n", dist)  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
print("rvecs旋转（向量）外参:\n", rvecs)  # 旋转向量  # 外参数
print("tvecs平移（向量）外参:\n", tvecs)  # 平移向量  # 外参数
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (u, v), 0, (u, v))
print('newcameramtx外参', newcameramtx)
print("写入文件名称:", file_path)