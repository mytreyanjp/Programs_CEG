import socket

def start_client(host='localhost', port=8080):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Sending a single HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        print("Sending request...")
        client_socket.sendall(request.encode())
        
        # Receiving the response
        response = client_socket.recv(4096).decode()
        print(f"Response from server:\n{response}\n")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")

if __name__ == "__main__":
    start_client()
