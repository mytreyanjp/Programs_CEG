import socket

def start_udp_echo_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendto(message.encode(), (host, port))
            data, _ = client_socket.recvfrom(1024)
            print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    start_udp_echo_client()
