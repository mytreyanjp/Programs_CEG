import socket
import time

def start_client(host='localhost', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        for i in range(3):  # Sending 3 requests
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: keep-alive\r\n\r\n"
            print(f"Sending request {i+1}...")
            client_socket.sendall(request.encode())
            
            response = client_socket.recv(4096).decode()
            print(f"Response from server:\n{response}\n")
            time.sleep(1)  # Sleep for a second before sending the next request

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")

if __name__ == "__main__":
    start_client()
