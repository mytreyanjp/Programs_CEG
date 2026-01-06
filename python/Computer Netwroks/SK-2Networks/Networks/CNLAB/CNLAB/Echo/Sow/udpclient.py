import socket

def start_udp_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print("Connected to UDP server. Type 'exit' to quit.")
        
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                print("Exiting...")
                break
            client_socket.sendto(message.encode(), (host, port))
            data, _ = client_socket.recvfrom(1024)
            print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    start_udp_client()


