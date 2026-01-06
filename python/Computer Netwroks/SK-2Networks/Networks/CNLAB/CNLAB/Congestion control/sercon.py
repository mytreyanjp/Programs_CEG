import socket

# Server parameters
server_host = '127.0.0.1'
server_port = 5000

# Set up and start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)
print("Server is listening on port", server_port)

client_socket, client_address = server_socket.accept()
print("Connection from", client_address)

while True:
    try:
        # Receive packet from client
        packet = client_socket.recv(1024).decode()
        if packet == 'end':
            print("Client has ended the transmission.")
            break
        
        print("Received:", packet)

        # Send acknowledgment for the received packet
        ack = f"ACK: {packet.split(':')[1]}"
        client_socket.send(ack.encode())
    except Exception as e:
        print("Error:", e)
        break

client_socket.close()
server_socket.close()
