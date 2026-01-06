import socket

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        if not request:
            return  # No data, exit the function

        print(f"Received request:\n{request}")

        # Basic HTTP response
        response_body = "Hello, World! This is a non-persistent connection."
        response_headers = "HTTP/1.1 200 OK\r\n" \
                           "Content-Type: text/plain\r\n" \
                           "Content-Length: {}\r\n" \
                           "Connection: close\r\n" \
                           "\r\n".format(len(response_body))

        # Send the response
        client_socket.sendall(response_headers.encode() + response_body.encode())
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

def server_start(host='localhost', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    server_start()
