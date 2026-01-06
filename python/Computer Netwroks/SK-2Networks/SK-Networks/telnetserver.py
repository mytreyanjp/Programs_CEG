import socket

def handle_client(client_socket):
    client_socket.sendall(b"Welcome to the Telnet Server!\n")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            send = input()
            response = f"They said: {send}\n"
            client_socket.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            break
    client_socket.close()

def start_server(host='0.0.0.0', port=2323):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
