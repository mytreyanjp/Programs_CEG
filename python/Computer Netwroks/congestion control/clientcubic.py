import socket
import os
import time
import random
import math


HOST = 'localhost'
PORT = 12346
IMAGE_FILE = 'space.jpg'
MAX_BUFFER = 3*10240

class CUBICSender:
    def __init__(self):
        self.cwnd = 10240
        self.ssthresh = float('inf')
        self.c = 0.4
        self.K = 0
        self.t0 = time.time()
        self.w_max = self.cwnd
        self.w_cubic = self.cwnd
    
    def update_cwnd(self, packet_loss):
        t = time.time() - self.t0
        if packet_loss:
            print(f"Packet loss detected. Reducing CWND from {self.cwnd}.")
            self.w_max = self.cwnd
            self.ssthresh = max(self.cwnd // 2, 1024)
            self.cwnd = max(1024, self.cwnd // 2)
            self.K = ((self.w_max - self.cwnd) / self.c) ** (1 / 3)
            self.t0 = time.time()

        else:

            delta_t = time.time() - self.t0
            cubic_growth = self.c * (delta_t - self.K) ** 3 + self.w_max
            self.w_cubic = max(1024, int(cubic_growth))
            
            if self.cwnd < self.ssthresh:
                self.cwnd += 1024
            else:
                self.cwnd = min(self.cwnd + 1024, self.w_cubic)

        print(f"Updated CWND: {self.cwnd}, CUBIC window: {self.w_cubic}")

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

    cubic_sender = CUBICSender()
    node = Node()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                total_size = len(image_data)
                print(f"Starting to send image of size {total_size} bytes using TCP CUBIC.")

                i = 0
                while i < total_size:

                    chunk_size = min(cubic_sender.cwnd, total_size - i)
                    if chunk_size <= 0:
                        print("No more data to send.")
                        break

                    chunk = image_data[i:i + chunk_size]
                    print(f"Preparing to send chunk of size {len(chunk)} bytes (CWND={cubic_sender.cwnd})")


                    packet_loss = random.random() <0.9


                    cubic_sender.update_cwnd(packet_loss)

                    if packet_loss:
                        cubic_sender.update_cwnd(True)
                        print("Simulated packet loss; skipping sending this chunk.")
                        continue


                    node.update_buffer_usage(len(chunk))
                    if node.buffer_usage > node.buffer_size:
                        node.drop_packet()
                        break


                    client_socket.sendall(chunk)
                    print(f"Sent chunk: {len(chunk)} bytes (CWND={cubic_sender.cwnd})")
                    
                    time.sleep(0.01)


                    i += chunk_size  

                print("Image sent successfully using TCP CUBIC.")

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
