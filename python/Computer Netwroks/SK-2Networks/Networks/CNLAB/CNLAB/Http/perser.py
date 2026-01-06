import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break  # No data, exit the loop
            
            print(f"Received request:\n{request}")

            # Basic HTTP response
            response_body = "Hello, World! This is a persistent connection."
            response_headers = "HTTP/1.1 200 OK\r\n" \
                               "Content-Type: text/plain\r\n" \
                               "Content-Length: {}\r\n" \
                               "Connection: keep-alive\r\n" \
                               "\r\n".format(len(response_body))

            # Send the response
            client_socket.sendall(response_headers.encode() + response_body.encode())

            # If you want to close after one request, uncomment the next line
            # break

        except Exception as e:
            print(f"Exception: {e}")
            break

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
        handler = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
        handler.start()

if __name__ == "__main__":
    server_start()
