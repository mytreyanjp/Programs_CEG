import socket

def handle_client(client_socket):
    expected_packet = 0
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
        packet_content = data.decode('utf-8')
        print(f"Received: {packet_content}")
        
        # Send an acknowledgment back to the client
        ack_message = f'ACK {expected_packet}'
        client_socket.sendall(ack_message.encode('utf-8'))
        expected_packet += 1

def main():
    server_address = ('localhost', 65433)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Server listening...")
        connection, client_address = server_socket.accept()
        
        with connection:
            print(f"Connection from {client_address}")
            buffer = ""
            while True:
                data = connection.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    packet, buffer = buffer.split('\n', 1)  # Split on newline
                    print(f"Received: {packet.strip()}")
										#handle_client(connection)
                
if __name__ == "__main__":
    main()

