import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"Client {addr} connected")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received message from {addr}: {message.decode()}")
            broadcast(message, client_socket)
    finally:
        print(f"Client {addr} disconnected")
        clients.remove(client_socket)
        client_socket.close()

def broadcast(message, source_socket):
    for client in clients:
        if client != source_socket:
            client.send(message)

def handle_server_input():
    while True:
        message = input("Server: ")
        if message.lower() == 'exit':
            break
        broadcast(message.encode(), None)

def start_tcp_chat_server(host='localhost', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"TCP Chat Server listening on {host}:{port}")

        input_thread = threading.Thread(target=handle_server_input)
        input_thread.start()

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == "__main__":
    start_tcp_chat_server()
