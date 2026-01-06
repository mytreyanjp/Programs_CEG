import socket
import random
import time

# DNS resolution
domain = "example.com"
ip_address = socket.gethostbyname(domain)
print(f"Resolved IP address for {domain}: {ip_address}")

# File to send
file_path = "large_file.txt"  # Ensure this file is at least 1MB for testing

# Connection parameters
tcp_port = 12345
udp_port = 12345
server_address = (ip_address, tcp_port)

# Set up TCP and UDP sockets
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to the server with TCP
tcp_client.connect(server_address)
print("Connected to the server via TCP")

# Simulating congestion control for TCP
window_size = 1  # Start window size
timeout_probability = 0.2  # 20% chance of timeout

# Open the file and read the content
with open(file_path, "rb") as file:
    file_data = file.read()
    halfway_point = len(file_data) // 2

# TCP transfer for the first half
print("Starting TCP transfer with congestion control...")
index = 0
while index < halfway_point:
    for _ in range(window_size):
        if index >= halfway_point:
            break
        packet = file_data[index:index + 1024]
        tcp_client.send(packet)
        print(f"Sent TCP packet: {index//1024 + 1} with window size {window_size}")
        index += 1024
    
    # Simulating acknowledgment and congestion control
    ack = tcp_client.recv(1024)
    if ack.decode() == "ACK":
        print("Received ACK")
        if random.random() < timeout_probability:
            print("Timeout occurred, halving window size.")
            window_size = max(1, window_size // 2)
        else:
            window_size += 1  # Increase window size if no timeout
    time.sleep(0.1)  # Simulate network delay

# UDP transfer for the second half
print("Switching to UDP transfer...")
udp_client_address = (ip_address, udp_port)

index = halfway_point
while index < len(file_data):
    packet = file_data[index:index + 1024]
    udp_client.sendto(packet, udp_client_address)
    print(f"Sent UDP packet: {index//1024 + 1}")
    index += 1024
    time.sleep(0.05)  # Simulate network delay

# Close sockets
tcp_client.close()
udp_client.close()
print("File transfer complete. Client connection closed.")
