import socket
import threading

HOST = '127.0.0.1' 
PORT = 12000       

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[DISCONNECTED] {client_address} disconnected.")
                break

            print(f"[{client_address}] {message}")
            
            client_socket.send(f"Server received: {message}".encode('utf-8'))

        except ConnectionResetError:
            print(f"[ERROR] Connection reset by {client_address}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
