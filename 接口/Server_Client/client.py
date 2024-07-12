# client.py
import socket  # 该模块提供了创建和操作网络套接字的功能
import struct  # 用于处理不同二进制数据类型之间的转换
import time

def main():
    # 创建一个TCP套接字。socket.AF_INET指定使用IPv4地址，socket.SOCK_STREAM指定使用面向流的套接字（即TCP）
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 客户端尝试连接到指定的服务器IP地址和端口号（在这里是12345）。SERVER_IP是一个占位符，你需要将其替换为实际服务器的IP地址
    client_socket.connect(('0.0.0.0', 12345))  # 替换为服务器的IP地址

    while True:
        # 发送三维坐标数据
        coords = [1.0, 2.0, 3.0]  # 这里替换为实际的三维坐标数据

        # 使用struct.pack将三维坐标列表转换为二进制格式的数据。格式字符串'3f'表示列表中有三个浮点数（float）
        data = struct.pack('3f', *coords)

        # 将打包后的二进制数据发送到服务器。sendall方法确保所有数据都被发送，即使需要分成多个数据包
        client_socket.sendall(data)

        print(f"Sent coordinates: {coords}")

        time.sleep(1)  # 一秒发送一次，根据需要调整

if __name__ == "__main__":
    main()