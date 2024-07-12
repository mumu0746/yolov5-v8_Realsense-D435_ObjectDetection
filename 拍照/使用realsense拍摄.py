import pyrealsense2 as rs
import cv2
import numpy as np

# 创建 RealSense 管道
pipeline = rs.pipeline()

# 创建配置并启用流
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 启动管道
pipeline.start(config)

# 创建对齐对象
align_to = rs.stream.color
align = rs.align(align_to)

fps=120
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
writer=cv2.VideoWriter('./video/001.mp4',fourcc,fps,(640,480))

try:
    while True:
        # 等待一帧图像
        frames = pipeline.wait_for_frames()
        # 对齐深度和彩色图像
        aligned_frames = align.process(frames)
        # 获取对齐后的彩色帧和深度帧
        color_frame = aligned_frames.first(rs.stream.color)
        # 将 RealSense 帧转换为 OpenCV 格式
        color_image = np.asanyarray(color_frame.get_data())  # RGB图
        
        # 写入视频文件
        writer.write(color_image)

        # 显示图像
        cv2.imshow('RealSense Video Stream', color_image)
        
        # 按下 Esc 退出
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    # 停止流并释放资源
    pipeline.stop()
    writer.release()
    cv2.destroyAllWindows()
