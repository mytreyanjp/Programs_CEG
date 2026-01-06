import socket

def start_server():
    host = '127.0.0.1'  # Localhost
    port = 4000         # Arbitrary non-privileged port

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    print(f"Server listening on {host}:{port}")

    while True:
        # Receive data from the client
        data, address = server_socket.recvfrom(1024)
        print(f"Received message: {data.decode()}")

        # Send response back to the client
        response = "Hello, client!"
        server_socket.sendto(response.encode(), address)

if __name__ == "__main__":
    start_server()