import socket
import time
import random
import threading

# Client parameters
server_host = '127.0.0.1'
server_port = 56781
packet_loss_prob = 0.2  # Simulate packet loss probability

# AIMD parameters
max_window_size = 64  # Maximum congestion window size
multiplicative_decrease = 0.5  # Cut window size by half on packet loss
num_packets = 50  # Total packets to send

def client_send(client_id):
    # Each client maintains its own parameters
    congestion_window = 1  # Initial congestion window size
    ssthresh = max_window_size  # Slow start threshold

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1.0)  # Set a 1-second timeout for ACK
    client_socket.connect((server_host, server_port))
    print(f"Client {client_id}: Connected to server")

    packet_id = 1  # Packet counter

    while packet_id <= num_packets:
        print(f"\nClient {client_id}: Attempting to send packets with congestion window: {congestion_window}")
        packets_sent = 0  # Track packets sent per congestion window
        successful_ack = True  # Track if all packets in this round were acknowledged

        # Send all packets within the current congestion window size
        while packets_sent < congestion_window and packet_id <= num_packets:
            # Simulate packet loss by randomly dropping packets
            if random.random() < packet_loss_prob:
                print(f"Client {client_id}: Packet {packet_id} lost! (Simulated)")
                congestion_window = max(1, int(congestion_window * multiplicative_decrease))
                ssthresh = congestion_window
                successful_ack = False  # Indicate a packet was lost in this round
                break  # Exit to adjust the window size and retransmit lost packet

            # Send packet
            packet = f"Client {client_id} Packet:{packet_id}"
            client_socket.send(packet.encode())
            print(f"Client {client_id}: Sent: {packet}")

            # Try to receive acknowledgment
            try:
                ack = client_socket.recv(1024).decode()
                print(f"Client {client_id}: Received:", ack)
                packet_id += 1  # Move to the next packet
                packets_sent += 1  # Update packets sent in this window
            except socket.timeout:
                print(f"Client {client_id}: Timeout! Packet {packet_id} not acknowledged. Retransmitting...")
                congestion_window = max(1, int(congestion_window * multiplicative_decrease))
                ssthresh = congestion_window
                successful_ack = False  # Indicate timeout in this round
                break  # Retransmit the current packet in the next round

        # Increase congestion window after a successful round
        if successful_ack:
            if congestion_window < ssthresh:
                # Slow start phase: double the congestion window
                congestion_window = min(congestion_window * 2, max_window_size)
            else:
                # Congestion avoidance phase: increase linearly by 1
                congestion_window = min(congestion_window + 1, max_window_size)

        # Add a small delay to simulate network conditions
        time.sleep(0.5)

    # Notify the server to end transmission
    client_socket.send("end".encode())
    client_socket.close()
    print(f"Client {client_id}: Transmission completed.")

if __name__ == "__main__":
    # Start multiple clients
    num_clients = 3  # Change this to the desired number of clients
    for i in range(num_clients):
        threading.Thread(target=client_send, args=(i + 1,)).start()
