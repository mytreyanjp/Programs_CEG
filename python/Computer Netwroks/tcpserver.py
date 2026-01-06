import socket

# Set up the final server (Node 5)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12347))  # Bind to localhost and port 12350
server_socket.listen(1)

print("Final Server (Node 5) is waiting for a connection...")

# Accept a client connection (through intermediate nodes)
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive data from the final intermediate node
data = client_socket.recv(1024)  # Buffer size of 1024 bytes
print(f"Received data at the final server: {data.decode()}")

# Send data back to the client
client_socket.send("Hello from the final server!".encode())

# Close the connection
client_socket.close()
server_socket.close()
