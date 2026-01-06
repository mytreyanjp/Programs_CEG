import matplotlib.pyplot as plt
import random

initial_cwnd = 1
max_cwnd = 64
init_threshold = 16
ssthresh = init_threshold
rounds = 50

def tcp_tahoe():
    cwnd = initial_cwnd
    ssthresh = 16
    cwnd_values = []

    for round in range(rounds):
        cwnd_values.append(cwnd)
        if cwnd < ssthresh:
            print(f"In slowstart: {cwnd}")
            cwnd *= 2
        else:
            print(f"In congestion avoidance: {cwnd}")
            cwnd += 1
        if cwnd > init_threshold and random.random() < 0.2:
            ssthresh = min(cwnd,init_threshold)
            cwnd = 1  
            print(f"PACKET LOSS - new threshold: {ssthresh}")
        cwnd = min(cwnd, max_cwnd)

    return cwnd_values

def tcp_reno():
    cwnd = initial_cwnd
    ssthresh = 16
    cwnd_values = []

    for round in range(rounds):
        cwnd_values.append(cwnd)
        if cwnd < ssthresh:
            print(f"In slowstart: {cwnd}")
            cwnd *= 2
        else:
            print(f"In congestion avoidance: {cwnd}")
            cwnd += 1
        if cwnd > init_threshold  and random.random() < 0.2:
            ssthresh = min(cwnd,init_threshold)
            cwnd = ssthresh//2
            print(f"PACKET LOSS - new threshold: {ssthresh}")
        cwnd = min(cwnd, max_cwnd)

    return cwnd_values
print("SImulating TAHOE")
tahoe_cwnd = tcp_tahoe()
print("SImulating RENO")
reno_cwnd = tcp_reno()
avg_tahoe = sum(tahoe_cwnd) / len(tahoe_cwnd)
avg_reno = sum(reno_cwnd) / len(reno_cwnd)


plt.figure(figsize=(12, 6))
plt.plot(tahoe_cwnd, label='TCP Tahoe', marker='o')
plt.plot(reno_cwnd, label='TCP Reno', marker='x')
plt.title('TCP Tahoe vs TCP Reno - Congestion Window Size Over Time')
plt.xlabel('Number of transmissions (RTT)s')
plt.ylabel('Congestion Window (cwnd)')
plt.axhline(y=avg_tahoe, color='blue', linestyle='--', label=f'Avg Tahoe: {avg_tahoe:.2f}')
plt.axhline(y=avg_reno, color='orange', linestyle='--', label=f'Avg Reno: {avg_reno:.2f}')
plt.legend()
plt.grid()
plt.ylim(0, max_cwnd + 10)
plt.xticks(range(rounds))
plt.show()