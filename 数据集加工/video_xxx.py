import cv2
import os
import sys

def extract_frames(video_path, output_folder, skip_frames=4):
    output_folder = "actual_pallet"
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 打开视频文件
    video = cv2.VideoCapture("50.mp4")
    
    # 检查视频是否成功打开
    if not video.isOpened():
        print("Error: Could not open video.")
        return
    
    frame_count = 21892  # 用于保存图片的计数器
    skip_count = 0   # 用于跟踪跳过的帧数

    while True:
        # 读取视频的下一帧
        ret, frame = video.read()
        
        # 如果正确读取帧，ret为True
        if not ret:
            print("Reached end of video or cannot fetch the frame.")
            break
        
        # 每三帧保存一次图片
        if skip_count == 0:
            # 构建图片保存路径
            frame_filename = os.path.join(output_folder, f"{frame_count:05d}.jpg")
            # 保存帧为图片
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")
            frame_count += 1
        
        # 更新跳过的帧数
        skip_count = (skip_count + 1) % skip_frames

    # 释放视频对象
    video.release()
    print("Video processing completed.")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python video_xxx.py <video_path> <output_folder> [<skip_frames>]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_folder = sys.argv[2]
    skip_frames = int(sys.argv[3]) if len(sys.argv) == 20 else 10  # 默认值为10
    print(skip_frames)
    
    extract_frames(video_path, output_folder, skip_frames)
