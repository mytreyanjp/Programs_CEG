import socket
import threading

def receive_messages(client_socket):
    while True:
        message, _ = client_socket.recvfrom(1024)
        print(f"\n{message.decode()}")

def start_udp_chat_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.sendto(message.encode(), (host, port))

if __name__ == "__main__":
    start_udp_chat_client()
