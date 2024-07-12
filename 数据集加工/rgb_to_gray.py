from PIL import Image
import os
from tqdm import tqdm

# 输入文件夹路径
input_folder = 'rgb_经过去杂质之后的照片'
# 输出文件夹路径
output_folder = 'gray_经过去杂质之后的照片'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取输入文件夹中所有文件的数量
total_files = len([name for name in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, name))])

# 使用tqdm创建进度条
for filename in tqdm(os.listdir(input_folder), total=total_files):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # 构建完整的文件路径
        file_path = os.path.join(input_folder, filename)
        
        # 打开图片
        with Image.open(file_path) as img:
            # 转换为灰度图
            grayscale_img = img.convert('L')
            
            # 构建输出文件的路径
            output_path = os.path.join(output_folder, filename)
            
            # 保存灰度图
            grayscale_img.save(output_path)

print("所有图片已转换为灰度图并保存。")