import socket
import time

def go_back_n_server(host='127.0.0.1', port=65432, window_size=4, total_packets=10):
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server is waiting for connection...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            base = 0  
            next_seq_num = 0  
            window = [] 

            packets = [f"Packet {i+1}" for i in range(total_packets)]

            while base < total_packets:
                while next_seq_num < base + window_size and next_seq_num < total_packets:
                    packet = packets[next_seq_num]
                    conn.sendall(packet.encode())
                    print(f"Sent: {packet}")
                    window.append(packet)
                    next_seq_num += 1
                
                try:
                    conn.settimeout(5.0)
                    ack = conn.recv(1024).decode()
                    print(f"Received ACK for: {ack}")
                    ack_num = int(ack.split()[1])  
                    
                    if ack_num > base:
                        base = ack_num  

                    window = window[ack_num - base:]  
                except socket.timeout:
                    print(f"Timeout occurred, resending from packet {base + 1}")
                    
                    next_seq_num = base

if __name__ == "__main__":
    go_back_n_server()

