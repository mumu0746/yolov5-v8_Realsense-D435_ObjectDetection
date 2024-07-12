# server.py
import socket  #用于创建和操作网络套接字
import struct  #用于进行二进制数据的打包和解包

def main():
    # 创建一个TCP套接字。socket.AF_INET指定使用IPv4地址，socket.SOCK_STREAM指定使用面向流的套接字（即TCP）
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 将服务器套接字绑定到IP地址0.0.0.0和端口号12345,端口号12345是一个占位符，你可以根据需要更改它
    server_socket.bind(('0.0.0.0', 12345))  # 使用0.0.0.0允许任何IP的连接

    # 使服务器套接字进入监听状态，准备接受客户端的连接请求
    server_socket.listen()

    while True:
        print("Waiting for a connection...")

        # 接受一个连接请求，conn是与客户端建立的连接的套接字，addr是客户端的地址
        conn, addr = server_socket.accept()

        # 使用上下文管理器来确保在代码块执行完毕后，无论是否发生异常，连接都会被正确关闭
        with conn:
            # 打印一条消息到控制台，显示连接的客户端的地址
            print(f"Connected by {addr}")

            while True:
                try:
                    # 假设三维坐标数据是3个float类型
                    # 使用recv方法从客户端接收数据。struct.calcsize('3f')计算一个包含三个浮点数的二进制数据所需的字节数，确保接收足够的数据
                    data = conn.recv(struct.calcsize('3f'))

                    # 检查接收到的数据是否为空，为空则跳出循环
                    if not data:
                        break

                    # 使用struct.unpack将接收到的二进制数据解包为三个浮点数，这些浮点数代表三维坐标
                    coords = struct.unpack('3f', data)

                    print(f"Received coordinates: {coords}")

                # 捕获所有异常，并将其存储在变量e中
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

if __name__ == "__main__":
    main()