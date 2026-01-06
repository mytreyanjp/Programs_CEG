import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            message = data.decode()
            print(f"Received from server: {message}")
        except socket.error as e:
            print(f"Socket error: {e}")
            break

def start_client_udp_chat(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((host,port))  # Bind to an available port

    # Start receiving messages in a separate thread
    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receiver_thread.daemon = True
    receiver_thread.start()

    try:
        while True:
            message = input("Enter message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendto(message.encode(), (host, port))
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
    finally:
        client_socket.close()
        print("Client is shutting down...")

if __name__ == "__main__":
    start_client_udp_chat()
