import socket
import time

def stop_and_wait_client(server_ip, server_port, data_packets):
    # Use TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("Connected to server")
    
    for packet in data_packets:
        try:
            # Send packet
            client_socket.sendall(packet.encode())
            print(f"Sent: {packet}")
            
            # Wait for acknowledgment
            client_socket.settimeout(1)
            ack = client_socket.recv(1024).decode()
            print(f"Received: {ack}")
        except socket.timeout:
            print("Timeout, resending...")
            client_socket.sendall(packet.encode())
    
    client_socket.close()
    print("Connection closed")

# Data packets to send
data_packets = [f"Packet {i}" for i in range(5)]
stop_and_wait_client('localhost', 12345, data_packets)
