import matplotlib.pyplot as plt
import numpy as np
import random

class TCP:
    def __init__(self, protocol, ssthresh=16, max_time=50):
        self.protocol = protocol
        self.ssthresh = ssthresh
        self.cwnd = 1
        self.time = 0
        self.max_time = max_time
        self.cwnd_history = []
        self.avg_cwnd_history = []

    def simulate(self):
        while self.time < self.max_time:
            self.cwnd_history.append(self.cwnd)
            self.avg_cwnd_history.append(np.mean(self.cwnd_history))
            self.time += 1

            if random.random() < 0.1:
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

tcp_tahoe = TCP(protocol='Tahoe', ssthresh=16, max_time=50)
tcp_reno = TCP(protocol='Reno', ssthresh=16, max_time=50)

tcp_tahoe.simulate()
tcp_reno.simulate()

plt.figure(figsize=(10, 6))
tcp_tahoe.plot()
tcp_reno.plot()

plt.xlabel('Time (units)')
plt.ylabel('Congestion Window Size (cwnd)')
plt.title('TCP Tahoe and Reno Congestion Control')
plt.legend()
plt.grid(True)
plt.show()
