import socket

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(('10.0.0.149', 12345))

while True:
    msg = input("请输入要发送的消息：")
    if msg == "exit":
        break
    socket_client.send(msg.encode('utf-8'))
    recv_data = socket_client.recv(1024).decode('utf-8')
    print("接收到消息：", recv_data)

socket_client.close()
