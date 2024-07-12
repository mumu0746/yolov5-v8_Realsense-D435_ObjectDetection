def input_point():
    """输入三维坐标点，并返回一个包含三个浮点数的元组。"""
    print("请输入三维坐标点 (x y z)，每输入一个数字后按回车键：")
    x = float(input("请输入x坐标："))
    y = float(input("请输入y坐标："))
    z = float(input("请输入z坐标："))
    return (x, y, z)

def calculate_distance(point1, point2):
    """计算两个三维坐标点之间的欧几里得距离。"""
    return ((point1[0] - point2[0]) ** 2 + 
            (point1[1] - point2[1]) ** 2 + 
            (point1[2] - point2[2]) ** 2) ** 0.5

# 获取用户输入的两个点
point1 = input_point()
point2 = input_point()

# 计算距离
distance = calculate_distance(point1, point2)

# 输出结果
print(f"两个点空间距离是：{distance:.2f}")