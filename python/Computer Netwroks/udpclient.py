import socket

def start_client():
    host = '127.0.0.1'  # Localhost
    port = 4000         # Arbitrary non-privileged port

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send a message to the server
    message = input("Enter your message: ")
    client_socket.sendto(message.encode(), (host, port))

    # Receive response from the server
    response, address = client_socket.recvfrom(1024)
    print(f"Received response: {response.decode()}")

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    start_client()