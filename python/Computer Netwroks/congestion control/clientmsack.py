import socket
import os
import time
import random


HOST = 'localhost'
PORT = 12346
IMAGE_FILE = 'space.jpg'
MAX_BUFFER = 3*10240

class MSACKSender:
    def __init__(self):
        self.cwnd = 10240
        self.sacks = set()
        self.slow_start = True

    def update_cwnd(self, acked_packets):
        if not acked_packets:
            print(f"Packet loss detected. Halving CWND from {self.cwnd}.")
            self.cwnd = max(1024, self.cwnd // 2)
            self.slow_start = False
        else:
            if self.slow_start:
                self.cwnd += 256
            else:
                self.cwnd += 128

    def register_sack(self, segment):
        self.sacks.add(segment)
        print(f"SACK received for segment: {segment}")

class Node:
    def __init__(self, buffer_size=MAX_BUFFER):
        self.buffer_size = buffer_size
        self.buffer_usage = 0

    def update_buffer_usage(self, packet_size):
        self.buffer_usage = min(self.buffer_size, self.buffer_usage + packet_size)

    def drop_packet(self):
        print("Packet dropped due to buffer overflow.")

def send_image(image_path):

    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    msack_sender = MSACKSender()
    node = Node()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                total_size = len(image_data)
                print(f"Starting to send image of size {total_size} bytes using mSACK.")

                i = 0
                while i < total_size:
                    chunk_size = min(msack_sender.cwnd, total_size - i)
                    chunk = image_data[i:i + chunk_size]
                    print(f"Preparing to send chunk of size {len(chunk)} bytes (CWND={msack_sender.cwnd})")


                    packet_loss = random.random() < 0.4

                    if packet_loss:
                        print("Simulated packet loss; skipping sending this chunk.")
                        msack_sender.update_cwnd(acked_packets=False)
                        continue


                    if random.random() < 0.3:
                        msack_sender.register_sack(i)


                    node.update_buffer_usage(len(chunk))
                    if node.buffer_usage > node.buffer_size:
                        node.drop_packet()
                        break


                    client_socket.sendall(chunk)
                    print(f"Sent chunk: {len(chunk)} bytes (CWND={msack_sender.cwnd})")
                    

                    time.sleep(0.01)


                    extra_processing_time = random.uniform(0.005, 0.015)
                    time.sleep(extra_processing_time)


                    msack_sender.update_cwnd(acked_packets=True)


                    i += chunk_size  

                print("Image sent successfully using mSACK.")

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    send_image(IMAGE_FILE)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
