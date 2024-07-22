import os
import shutil
from tqdm import tqdm

# 设置文件夹路径
json_folder = '标签汇总/1总标签数'
image_folder = 'rgb_pallet'
output_folder = '已外包出去的照片/0721训练9651张照片'

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取json文件夹中的文件名
json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

# 使用tqdm创建进度条
progress_bar = tqdm(total=len(json_files), desc='Copying images', unit='file')

# 遍历json文件名
for json_file in json_files:
    # 获取对应的图片文件名
    image_file = json_file.replace('.json', '.jpg')
    if image_file in os.listdir(image_folder):
        # 构建完整的文件路径
        image_path = os.path.join(image_folder, image_file)
        output_path = os.path.join(output_folder, image_file)
        
        # 复制文件
        shutil.copy(image_path, output_path)
        progress_bar.update(1)  # 更新进度条
    else:
        progress_bar.update(1)  # 即使没有找到匹配的图片，也更新进度条

progress_bar.close()  # 完成时关闭进度条
print("Process completed.")