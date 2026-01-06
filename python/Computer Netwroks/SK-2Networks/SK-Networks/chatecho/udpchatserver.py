import socket

def start_udp_chat_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Chat Server listening on {host}:{port}")

        clients = set()
        while True:
            message, addr = server_socket.recvfrom(1024)
            print(f"Received message from {addr}: {message.decode()}")
            if addr not in clients:
                clients.add(addr)
            for client in clients:
                if client != addr:
                    server_socket.sendto(message, client)

if __name__ == "__main__":
    start_udp_chat_server()
