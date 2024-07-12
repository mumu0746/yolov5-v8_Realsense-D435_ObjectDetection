import socket

socket_server = socket.socket()
socket_server.bind(('10.0.0.149', 12345))
socket_server.listen(1)

print('Waiting for connection...')

conn, addr = socket_server.accept()
print('Connected by', addr)

while True:
    data = conn.recv(1024).decode('UTF-8')
    print('Received:', data)
    msg = input('Send: ')
    conn.send(msg.encode('UTF-8'))
    if data == 'exit':
        break

conn.close()
socket_server.close()
