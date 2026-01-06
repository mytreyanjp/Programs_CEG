import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8081)
client_socket.connect(server_address)

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
client_socket.sendall(http_request.encode())

response = client_socket.recv(4096).decode()
print("Received response:", response)

client_socket.close()
