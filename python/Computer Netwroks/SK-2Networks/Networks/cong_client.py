# client.py
import socket
import json
import matplotlib.pyplot as plt
import numpy as np

class TCPClient:
    def __init__(self, protocol, ssthresh=16, max_time=50, port=8080):
        self.protocol = protocol
        self.ssthresh = ssthresh
        self.cwnd = 1
        self.time = 0
        self.max_time = max_time
        self.port = port
        self.cwnd_history = []
        self.avg_cwnd_history = []

    def simulate(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', self.port))
            while self.time < self.max_time:
                data = client_socket.recv(1024)
                if not data:
                    break

                # Process server response
                response = json.loads(data.decode())
                self.time = response['time']
                loss = response['loss']

                self.cwnd_history.append(self.cwnd)
                self.avg_cwnd_history.append(np.mean(self.cwnd_history))

                if loss:
                    print(f"[{self.protocol}] Packet loss at time {self.time}, cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")
                    if self.protocol == 'Tahoe':
                        self.ssthresh = max(2, self.cwnd // 2)
                        self.cwnd = 1
                    elif self.protocol == 'Reno':
                        if self.cwnd >= self.ssthresh:
                            self.ssthresh = max(2, self.cwnd // 2)
                            self.cwnd = self.ssthresh
                            print(f"[{self.protocol}] Fast Recovery, new cwnd: {self.cwnd}, new ssthresh: {self.ssthresh}")
                        else:
                            self.ssthresh = max(2, self.cwnd // 2)
                            self.cwnd = 1
                else:
                    if self.cwnd < self.ssthresh:
                        self.cwnd *= 2
                    else:
                        self.cwnd += 1

                self.cwnd = min(self.cwnd, 100)

    def plot(self):
        plt.plot(range(len(self.cwnd_history)), self.cwnd_history, label=f'{self.protocol} cwnd')
        plt.plot(range(len(self.avg_cwnd_history)), self.avg_cwnd_history, linestyle='--', label=f'{self.protocol} avg cwnd')

if __name__ == "__main__":
    tcp_client = TCPClient(protocol='Tahoe', ssthresh=16, max_time=50)
    tcp_client.simulate()
    
    plt.figure(figsize=(10, 6))
    tcp_client.plot()

    plt.xlabel('Time (units)')
    plt.ylabel('Congestion Window Size (cwnd)')
    plt.title('TCP Client Congestion Control')
    plt.legend()
    plt.grid(True)
    plt.show()
