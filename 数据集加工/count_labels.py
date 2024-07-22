import os
import json
from collections import defaultdict

def count_labels(folder_path):
    # 使用defaultdict来存储每种标签的计数，初始值为0
    label_counts = defaultdict(int)
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # 确保文件是JSON格式
            file_path = os.path.join(folder_path, filename)
            # 打开并读取JSON文件
            with open(file_path, 'r') as file:
                data = json.load(file)
                # 假设JSON文件中标签存储在'shapes'键下
                shapes = data.get('shapes', [])
                for shape in shapes:
                    label = shape.get('label')  # 获取标签
                    label_counts[label] += 1  # 对应标签计数加1

    return label_counts

all_labels = 0
# 指定包含JSON文件的文件夹路径
json_folder_path = 'json'  # 替换为你的JSON文件夹路径
# 调用函数并获取标签计数
label_counts = count_labels(json_folder_path)

print("")
# 打印每种标签的总数
for label, count in label_counts.items():
    print(f"'{label}': {count}")
    all_labels += count

print(f"标签总数: {all_labels}\n")