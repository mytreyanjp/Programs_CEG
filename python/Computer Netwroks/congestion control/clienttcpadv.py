import socket
import random
import time


HOST = 'localhost'
PORT = 12346
IMAGE_FILE = 'space.jpg'
MAX_BUFFER = 3*10240

class VehicularSender:
    def __init__(self):
        self.cwnd = 10240

    def update_cwnd(self, buffer_status, link_status):
        print(f"Buffer Status: {buffer_status}, Link Status: {link_status}, Current CWND: {self.cwnd}")
        
        if buffer_status == 0 and link_status == 0:
            print(f"Aggressive growth: CWND before: {self.cwnd}")
            self.cwnd = 2 * self.cwnd + 1
            print(f"Aggressive growth: CWND after: {self.cwnd}")
        elif buffer_status == 0 and link_status == 1:
            print(f"Additive increase: CWND before: {self.cwnd}")
            self.cwnd += 10
            print(f"Additive increase: CWND after: {self.cwnd}")
        elif buffer_status == 1 and link_status == 1:
            print(f"Subtractive decrease: CWND before: {self.cwnd}")
            self.cwnd = max(1, self.cwnd - 100)
            print(f"Subtractive decrease: CWND after: {self.cwnd}")

class Node:
    def __init__(self, buffer_size=MAX_BUFFER):
        self.buffer_size = buffer_size
        self.buffer_usage = 0

    def update_buffer_usage(self, packet_size):
        self.buffer_usage = min(self.buffer_size, self.buffer_usage + packet_size)
        print(f"Buffer usage updated to: {self.buffer_usage} bytes")
    
    def drop_packet(self):
        print("Packet dropped due to buffer overflow.")
    
    def drain_buffer(self, amount=512):

        time.sleep(random.uniform(0, 0.5))  
        self.buffer_usage = max(0, self.buffer_usage - amount)
        print(f"Buffer drained. Current buffer usage: {self.buffer_usage} bytes")

def send_image(image_path):
    vehicular_sender = VehicularSender()
    node = Node()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            total_size = len(image_data)
            print(f"Starting to send image of size {total_size} bytes using Vehicular method.")
            
            i = 0
            while i < total_size:
                chunk_size = min(vehicular_sender.cwnd, total_size - i)
                chunk = image_data[i:i + chunk_size]
                print(f"Preparing to send chunk of size {len(chunk)} bytes")
                time.sleep(0.001)


                node.update_buffer_usage(len(chunk))


                if node.buffer_usage > node.buffer_size:
                    node.drop_packet()



                buffer_status = 1 if node.buffer_usage > 0.7 * node.buffer_size else 0
                link_status = 1 if random.random() > 0.8 else 0


                vehicular_sender.update_cwnd(buffer_status, link_status)


                client_socket.sendall(chunk)  
                print(f"Sent chunk: {len(chunk)} bytes (CWND={vehicular_sender.cwnd})")
                node.drain_buffer()

                i += chunk_size

            print("Image sent successfully using Vehicular method.")


def main():
    send_image(IMAGE_FILE)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

