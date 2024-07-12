import cv2
import os

# 初始化单个外接摄像头
camera = cv2.VideoCapture(4)  # 通常笔记本电脑的内置摄像头是0，外接摄像头可能是1或其他数字

# 检查相机是否成功打开
if not camera.isOpened():
    print("Unable to open camera, please check the camera index or connection.")
    exit()

# 创建存储照片的文件夹，如果不存在则创建
folder = "./captures/"
os.makedirs(folder, exist_ok=True)

i = 1

try:
    while True:
        # 读取相机的图像
        ret, frame = camera.read()

        # 检查是否成功读取图像
        if not ret:
            print("Failed to capture video from the camera.")
            break
        frame=cv2.flip(frame,1)
        # 显示实时画面
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        # 按 'q' 退出程序
        if key == ord('q'):
            break
        # 按 's' 保存图像
        elif key == ord('s'):
            filename = os.path.join(folder, f"capture_{i}.png")

            cv2.imwrite(filename, frame)
            print(f"Image saved! Filename: {filename}")
            i += 1

except KeyboardInterrupt:
    # 释放相机资源
    camera.release()
    # 关闭所有OpenCV窗口
    cv2.destroyAllWindows()

# 确保释放资源
finally:
    if camera is not None:
        camera.release()
    cv2.destroyAllWindows()
