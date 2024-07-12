import cv2
import numpy as np
import time
import random
import math

# 左镜头的内参，如焦距
left_camera_matrix = np.array([[462.133514336444,0,347.803590904120],[0,463.678615268928,219.407202691333],[0.,0.,1.]])
right_camera_matrix = np.array([[464.482539956047,0,330.094171485676],[0,464.783201593674,221.142074148110],[0.,0.,1.]])

# 畸变系数,K1、K2、K3为径向畸变,P1、P2为切向畸变
left_distortion = np.array([[-0.00497652311288390,0.0820352335664872,0.000437646721496926,0.00177246737843981,-0.0843373866767442]])
right_distortion = np.array([[0-0.0113596637560300,0.0867465575934141,0.00204309556967923,0.00250841974846738,-0.0661185696437842]])

# 旋转矩阵
R = np.array([[0.999184252354167,0.000227858840184140,0.0403828915234302],
              [0.000168677454339987,0.999951810297194,-0.00981573386363553],
              [-0.0403831820856229,0.00981453838518521,0.999136063527348]])
# 平移矩阵
T = np.array([-93.8831553787771,-0.459371019107153,-5.33567813419939])

size = (640, 480)


#立体矫正
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)

# 校正查找映射表,将原始图像和校正后的图像上的点一一对应起来
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)
print(Q)

#鼠标回调函数      
def onmouse_pick_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        threeD = param
        print('\n像素坐标 x = %d, y = %d' % (x, y))
        # print("世界坐标是：", threeD[y][x][0], threeD[y][x][1], threeD[y][x][2], "mm")
        print("世界坐标xyz 是：", threeD[y][x][0] / 1000.0, threeD[y][x][1] / 1000.0, threeD[y][x][2] / 1000.0, "m")

        distance = math.sqrt(threeD[y][x][0] ** 2 + threeD[y][x][1] ** 2 + threeD[y][x][2] ** 2)
        distance = distance / 1000.0  # mm -> m
        print("距离是：", distance, "m")


# 加载两个图片文件
capture_left = cv2.imread("captures9/capture_left_1.png")
capture_right = cv2.imread("captures9/capture_right_1.png")

if capture_left is None or capture_right is None:
    print("图片文件加载失败，请检查文件路径和文件完整性。")
    exit()

# 确保两个图片都已成功读取
ret_left, frame_left = True, capture_left
ret_right, frame_right = True, capture_right

WIN_NAME = 'Stereo Depth Estimation'
cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)

# 将BGR格式转换为灰度图像
imgL = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
imgR = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

# 重映射，校正图像
img1_rectified = cv2.remap(imgL, left_map1, left_map2, cv2.INTER_LINEAR)
img2_rectified = cv2.remap(imgR, right_map1, right_map2, cv2.INTER_LINEAR)

# SGBM算法参数
blockSize = 3
img_channels = 3
stereo = cv2.StereoSGBM_create(minDisparity=1,
                               numDisparities=64,
                               blockSize=blockSize,
                               P1=8 * img_channels * blockSize * blockSize,
                               P2=32 * img_channels * blockSize * blockSize,
                               disp12MaxDiff=-1,
                               preFilterCap=1,
                               uniquenessRatio=10,
                               speckleWindowSize=100,
                               speckleRange=100,
                               mode=cv2.STEREO_SGBM_MODE_HH)

# 计算视差
disparity = stereo.compute(img1_rectified, img2_rectified)

# 归一化视差图
disp = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 生成深度图（颜色图）
dis_color = cv2.applyColorMap(cv2.convertScaleAbs(disp), cv2.COLORMAP_JET)

# 计算三维坐标数据值
scale_factor = Q[2, 3]  # 这将给出与深度相关的缩放因子
threeD = cv2.reprojectImageTo3D(disparity, Q, handleMissingValues=True)
threeD = threeD * 12  # 缩放因子，将视差转换为实际距离

# 鼠标回调事件
cv2.setMouseCallback(WIN_NAME, onmouse_pick_points, threeD)

# 显示处理后的图像
cv2.imshow(WIN_NAME, dis_color)  # 显示深度图
cv2.imshow("left", imgL)  # 显示左相机的灰度图像
cv2.imshow("right", imgR)  # 显示右相机的灰度图像

# 等待用户按键操作
cv2.waitKey(0)

# 释放资源
cv2.destroyAllWindows()