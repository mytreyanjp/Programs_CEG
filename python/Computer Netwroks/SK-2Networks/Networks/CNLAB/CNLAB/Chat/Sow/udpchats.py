import socket
import threading

clients = set()
clients_lock = threading.Lock()

def handle_client(server_socket):
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode()

            with clients_lock:
                clients.add(addr)  # Add new clients to the set

                # Broadcast the message to all clients except the sender
                for client in clients:
                    if client != addr:
                        server_socket.sendto(data, client)
            print(f"Received from {addr}: {message}")
        except Exception as e:
            print(f"Socket error: {e}")
            break

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP Server listening on {host}:{port}")

    handler_thread = threading.Thread(target=handle_client, args=(server_socket,), daemon=True)
    handler_thread.start()

    try:
        while True:
            pass  # Keeps server running
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
