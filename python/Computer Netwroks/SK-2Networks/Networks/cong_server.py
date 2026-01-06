# server.py
import random
import socket
import json

class Server:
    def __init__(self, loss_probability=0.1, port=8080):
        self.loss_probability = loss_probability
        self.time = 0
        self.port = port
        self.max_time = 50
        self.ssthresh = 16

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', self.port))
            server_socket.listen(1)
            print(f"Server listening on port {self.port}")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected to {addr}")
                while self.time < self.max_time:
                    # Determine if there's packet loss
                    loss = random.random() < self.loss_probability
                    data = json.dumps({
                        'time': self.time,
                        'loss': loss
                    })
                    conn.sendall(data.encode())
                    print(f"[Server] Time: {self.time}, Loss: {loss}")
                    self.time += 1

if __name__ == "__main__":
    server = Server()
    server.start()
