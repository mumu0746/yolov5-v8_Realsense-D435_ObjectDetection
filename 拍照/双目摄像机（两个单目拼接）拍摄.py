import cv2
import os

# 初始化两个摄像头
# 左边摄像头是灰色的，无法进行标定
camera_left = cv2.VideoCapture(2)  # 内置摄像头通常是0

camera_right = cv2.VideoCapture(4)  # 外接摄像头通常是1

# 创建存储照片的文件夹，如果不存在则创建
folder = "./captures/"
os.makedirs(folder, exist_ok=True)

i = 1

if not (camera_left.isOpened() and camera_right.isOpened()):
    print("Unable to open one or both cameras, please check the camera index or connection.")
    exit()

try:
    while True:
        # 读取两个相机的图像
        ret_left, frame_left = camera_left.read()

        ret_right, frame_right = camera_right.read()

        # 检查是否成功读取图像
        if not (ret_left and ret_right):
            print("Failed to capture video from one or both cameras.")
            break

        # 翻转图像，使图像正向显示
        frame_left = cv2.flip(frame_left, 1)

        frame_right = cv2.flip(frame_right, 1)

        """
            修改左眼图片，使其恢复正常
        """
        print("左眼图片的通道数是:", frame_left.ndim)
        print("等于3则是RGB格式:", frame_left.shape[2])


        # 显示实时画面
        cv2.imshow("Camera Left", frame_left)
        cv2.imshow("Camera Right", frame_right)

        key = cv2.waitKey(1) & 0xFF

        # 按 'q' 退出程序
        if key == ord('q'):
            break
        # 按 's' 保存图像
        elif key == ord('s'):
            filename_left = os.path.join(folder, f"capture_left_{i}.png")
            filename_right = os.path.join(folder, f"capture_right_{i}.png")

            cv2.imwrite(filename_left, frame_left)
            cv2.imwrite(filename_right, frame_right)
            print(f"Images saved! Filenames: {filename_left}, {filename_right}")
            i += 1

except KeyboardInterrupt:
    # 释放相机资源
    camera_left.release()
    camera_right.release()
    # 关闭所有OpenCV窗口
    cv2.destroyAllWindows()

# 确保释放资源
finally:
    if camera_left is not None:
        camera_left.release()
    if camera_right is not None:
        camera_right.release()
    cv2.destroyAllWindows()
