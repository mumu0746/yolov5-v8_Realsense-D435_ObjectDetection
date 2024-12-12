import os
import cv2
import pyrealsense2 as rs
import numpy as np


def take_photo(color_frame, chess_path):
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(chess_path, color_image)
    print(f"照片已保存到: {chess_path}")

def main():
    # 创建保存照片的文件夹
    photo_dir = "chess"
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    # 配置相机
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # 启动相机
    profile = pipeline.start(config)

    try:
        photo_count = 0
        while True:
            # 等待帧
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # 将帧转换为图像
            color_image = np.asanyarray(color_frame.get_data())
            cv2.imshow('RealSense D435i 实时视频', color_image)

            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):
                chess_path = os.path.join(photo_dir, f"photo_{photo_count}.png")
                take_photo(color_frame, chess_path)
                photo_count += 1
            elif key == 27:  # 按下ESC键退出
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
