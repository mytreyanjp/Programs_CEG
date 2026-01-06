import socket
import threading

def receive(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            message = data.decode()

            print(f"Message received from server: {message}")
        except Exception as e:
            print(f"Exception: {e}")
            break

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    handler = threading.Thread(target=receive, args=(client_socket,), daemon=True)
    handler.start()

    try:
        while True:
            data1 = input("Enter message: ")
            
            if data1.lower() == 'exit':
                print("Exiting...")
                break

            client_socket.sendall(data1.encode())
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        client_socket.close()
        print("Client shutting down...")

if __name__ == "__main__":
    start_client()

#"123": "example.com",
    #"456": "openai.com",
    #"101": "github.com",
    #"102": "stackoverflow.com",
    #"103": "wikipedia.org",