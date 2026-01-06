import socket
import time
import random

INITIAL_WINDOW_SIZE = 1
MAX_WINDOW_SIZE = 8
CONGESTION_REDUCTION_FACTOR = 0.5
WINDOW_INCREMENT = 1

def generate_live_packet(index):
    return f"Packet {index}: {random.random()} at {time.time()}".encode('utf-8')

def send_packets_with_congestion_control(client_socket, num_packets):
    window_size = INITIAL_WINDOW_SIZE
    ack_received = 0
    unacknowledged_packets = {}

    while ack_received < num_packets:
        window_end = min(ack_received + window_size, num_packets)


        for i in range(ack_received, window_end):
            packet = generate_live_packet(i)
            print(f"Sending: {packet.decode('utf-8')}")
            client_socket.sendall(packet)
            unacknowledged_packets[i] = time.time()

        
        client_socket.settimeout(5.0) 
        try:
            while ack_received < window_end:
                ack = client_socket.recv(1024).decode('utf-8')
                print(f"Received ACK: {ack}")  

                if ack.startswith('ACK'):
                    parts = ack.split()
                    if len(parts) == 2 and parts[0] == 'ACK':
                        try:
                            ack_number = int(parts[1])
                            
                            if ack_number in unacknowledged_packets:
                                del unacknowledged_packets[ack_number]
                              
                                while ack_received <= ack_number:
                                    ack_received += 1
                            else:
                                print(f"Received ACK for unknown packet: {ack_number}")
                        except ValueError:
                            print("Malformed ACK received. Expected a number after 'ACK'.")

            
                current_time = time.time()
                for pkt_num in list(unacknowledged_packets.keys()):
                    if current_time - unacknowledged_packets[pkt_num] > 5.0: 
                        print(f"Retransmitting Packet {pkt_num}")
                        packet = generate_live_packet(pkt_num)
                        client_socket.sendall(packet)
                        unacknowledged_packets[pkt_num] = current_time  

           
            window_size = min(window_size + WINDOW_INCREMENT, MAX_WINDOW_SIZE)

        except socket.timeout:
            print("ACK timeout. Reducing window size...")
            window_size = max(int(window_size * CONGESTION_REDUCTION_FACTOR), INITIAL_WINDOW_SIZE)
            
            for i in range(ack_received, window_end):
                if i in unacknowledged_packets:
                    print(f"Retransmitting Packet {i}")
                    packet = generate_live_packet(i)
                    client_socket.sendall(packet)
                    unacknowledged_packets[i] = time.time()  

    print("All packets sent, closing connection.")
    client_socket.close()  

def main():
    server_address = ('localhost', 65431)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        num_packets = 10  # Adjust the number of packets as needed
        send_packets_with_congestion_control(client_socket, num_packets)

if __name__ == "__main__":
    main()

