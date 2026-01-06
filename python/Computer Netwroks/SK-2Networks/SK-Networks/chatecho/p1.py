import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print("Received:", msg)
                # Broadcast the message to all connected clients
                broadcast(msg, client_socket)
            else:
                break
        except:
            break
    client_socket.close()

def broadcast(msg, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg.encode())
            except:
                client.close()
                clients.remove(client)

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen(5)
print("Server started. Waiting for connections...")

clients = []

while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr} has been established.")
    clients.append(client_socket)

    # Start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()