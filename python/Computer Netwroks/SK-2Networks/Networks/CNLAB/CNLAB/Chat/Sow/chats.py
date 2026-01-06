import socket
import threading
clients = []
clients_lock = threading.Lock()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message: break
            print(f"Received: {message}")
            with clients_lock:
                for client in clients:
                    if client != client_socket:
                        client.sendall(message.encode())
        except Exception:
            break
    with clients_lock:
        clients.remove(client_socket)
    client_socket.close()

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with clients_lock:
                clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
        except KeyboardInterrupt:
            break

    for client in clients:
        client.close()
    server_socket.close()
    print("Server is shutting down...")

if __name__ == "__main__":
    start_server()
