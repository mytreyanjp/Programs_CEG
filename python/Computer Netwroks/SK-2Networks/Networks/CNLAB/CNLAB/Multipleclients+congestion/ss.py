import socket
import threading

# Server parameters
server_host = '127.0.0.1'
server_port = 56781

# Set up and start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(5)  # Allow up to 5 simultaneous connections
print("Server is listening on port", server_port)

def handle_client(client_socket, client_address):
    print("Connection from", client_address)
    
    while True:
        try:
            # Receive packet from client
            packet = client_socket.recv(1024).decode()
            if packet == 'end':
                print(f"Client {client_address} has ended the transmission.")
                break
            
            print(f"Received from {client_address}: {packet}")

            # Send acknowledgment for the received packet
            ack = f"ACK: {packet.split(':')[1]}"
            client_socket.send(ack.encode())
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()
    print(f"Connection closed with {client_address}")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
