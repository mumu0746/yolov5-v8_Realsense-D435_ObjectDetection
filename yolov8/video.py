from ultralytics import YOLO
import cv2
import pyrealsense2 as rs
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


model = YOLO(r"runs/segment/train/weights/v8_blue_seg_best.pt")  #模型初始化
# 加载 YOLOv8 模型


try:
    while True:
        # 等待一帧图像
        frames = pipeline.wait_for_frames()

        # 对齐深度和彩色图像
        aligned_frames = align.process(frames)

        # 获取对齐后的彩色帧和深度帧
        color_frame = aligned_frames.first(rs.stream.color)
        depth_frame = aligned_frames.get_depth_frame()

        # 将 RealSense 帧转换为 OpenCV 格式
        color_image = np.asanyarray(color_frame.get_data())  # RGB图
        depth_image = np.asanyarray(depth_frame.get_data())  # 深度图（默认16位）
        depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)  # 深度图（8位）
        depth_image_3d = np.dstack(
            (depth_image_8bit, depth_image_8bit, depth_image_8bit))  # 3通道深度图

        ############### 相机参数的获取 #######################
        intr = color_frame.profile.as_video_stream_profile().intrinsics  # 获取相机内参

        # 深度计算
        depth_intrin = depth_frame.profile.as_video_stream_profile(
        ).intrinsics  # 获取深度参数（像素坐标系转相机坐标系会用到）
        '''camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                            'ppx': intr.ppx, 'ppy': intr.ppy,
                            'height': intr.height, 'width': intr.width,
                            'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
                            }'''
        
         # 进行 YOLOv8 检测
        results = model(color_image, conf=0.7)  # 参数选择（置信度>=0.7才显示出来，可以自己调）
        annotated_frame = results[0].plot()     # （置信度最高的一帧图像取出来）
  
        # 显示图像
        cv2.imshow('Color Image', annotated_frame)

        # 按下 Esc 退出
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
