import socket

def handle_client(client_socket):
    """Handles client communication."""
    client_socket.sendall(b'Welcome to the Telnet Server!\n')
    
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received command: {data.strip()}")

            # Simple command handling
            if data.strip().lower() == 'quit':
                client_socket.sendall(b'Goodbye!\n')
                break
            elif data.strip().lower() == 'hello':
                client_socket.sendall(b'Hello, client!\n')
            else:
                client_socket.sendall(b'Unknown command.\n')
        except Exception as e:
            print(f"Error: {e}")
            break
    
    client_socket.close()

def start_server(host='localhost', port=4000):
    """Starts the Telnet server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Telnet server started on {host}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == '__main__':
    start_server()

