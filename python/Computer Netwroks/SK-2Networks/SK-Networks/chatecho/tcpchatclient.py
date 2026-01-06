import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\n{message.decode()}") 
        except:
            break

def start_tcp_chat_client(host='10.11.145.93', port=9999):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode())

        client_socket.close()

if __name__ == "__main__":
    start_tcp_chat_client()
