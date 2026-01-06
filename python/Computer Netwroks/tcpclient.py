import socket

# Set up client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))  # Connect to the first intermediate node

# Send data to the first node
client_socket.send("Hello through 5 intermediate nodes!".encode())

# Receive response from the final server
data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")

# Close the connection
client_socket.close()
