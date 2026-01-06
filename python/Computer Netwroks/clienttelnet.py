import socket

def start_client(host='127.0.0.1', port=4000):
    """Starts a Telnet client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(client_socket.recv(1024).decode('utf-8'), end='')  # Print welcome message

    while True:
        command = input("Enter command (type 'quit' to exit): ")
        client_socket.sendall(command.encode('utf-8'))

        # Receive response from server
        response = client_socket.recv(1024).decode('utf-8')
        print(response, end='')

        if command.strip().lower() == 'quit':
            break

    client_socket.close()

if __name__ == '__main__':
    start_client()

