import socket
import random

def go_back_n_client(host='127.0.0.1', port=65432, total_packets=10, loss_prob=0.2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        expected_seq_num = 1  
        received_packets = []  

        while expected_seq_num <= total_packets:
            try:
                packet = client_socket.recv(1024).decode().strip()  # Trim any leading/trailing whitespace
                print(f"Received: {packet}")

                # Safely split and parse the packet number
                parts = packet.split()
                if len(parts) < 2 or not parts[1].isdigit():
                    print(f"Invalid packet format received: {packet}")
                    continue
                
                packet_num = int(parts[1])  

                if random.random() < loss_prob:
                    print(f"Simulating packet loss for Packet {packet_num}")
                    continue

                if packet_num == expected_seq_num:
                    print(f"Packet {packet_num} is correct, sending ACK.")
                    received_packets.append(packet)
                    client_socket.sendall(f"ACK {packet_num}".encode())  
                    expected_seq_num += 1  
                else:
                    print(f"Out-of-order packet {packet_num}, expected {expected_seq_num}. Ignoring.")

            except socket.timeout:
                print("Client timeout waiting for packets.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    go_back_n_client()

