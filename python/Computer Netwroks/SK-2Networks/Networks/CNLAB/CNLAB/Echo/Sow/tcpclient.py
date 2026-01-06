import socket

def start_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode())
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode()}")

if __name__ == "__main__":
    start_client()
