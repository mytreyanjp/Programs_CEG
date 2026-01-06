import socket
import threading

# Dictionary mapping IDs to domain names
id_to_domain = {
    "123": "example.com",
    "456": "openai.com",
    "789": "python.org"
}

clients = set()
clients_lock = threading.Lock()

def handle_client(connection, address):
    print("Server running...")
    while True:
        try:   
            data = connection.recv(1024)
            msg = data.decode().strip()
            print(f"Message received from {address} as {msg}")

            with clients_lock:
                clients.add(connection)

                # Check if message is an ID and respond with the corresponding domain name
                if msg in id_to_domain:
                    response = f"Domain name for ID {msg}: {id_to_domain[msg]}"
                    connection.sendall(response.encode())
                else:
                    # Broadcast the message to other clients if not an ID
                    for client in clients:
                        if client != connection:
                            client.sendall(data)
                    print(f"Received from {address}: {msg}")
        except Exception as e:
            print(f"Exception: {e}")
            break

def server_start(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server started. Waiting for clients to connect...")

    try:
        while True:
            connection, address = server_socket.accept()
            print(f"Connection from {address}")
            handler = threading.Thread(target=handle_client, args=(connection, address), daemon=True)
            handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_start()
