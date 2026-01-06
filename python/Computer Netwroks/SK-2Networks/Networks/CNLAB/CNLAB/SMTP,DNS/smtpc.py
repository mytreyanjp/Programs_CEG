from socket import *

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1025

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"HELO example.com\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"MAIL FROM:<sender@example.com>\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"RCPT TO:<recipient@example.com>\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"DATA\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"Subject: Test Email\r\n")
client_socket.send(b"Hello, this is a test email.\r\n")
client_socket.send(b".\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.send(b"QUIT\r\n")
server_response = client_socket.recv(1024).decode()
print(f"Server: {server_response.strip()}")

client_socket.close()