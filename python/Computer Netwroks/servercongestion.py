import time
import random

class TCPSender:
    def __init__(self):
        self.cwnd = 1  # Congestion Window (initial size)
        self.ssthresh = 8  # Slow Start Threshold
        self.baseRTT = 0.1  # Base round-trip time
        self.simulated_loss_rate = 0.2  # Simulated packet loss rate
        self.dup_acks = 0  # Count of duplicate acknowledgments
        self.in_fast_recovery = False  # Flag for Fast Recovery

    def send_packet(self):
       
        if random.random() < self.simulated_loss_rate:
            return False  
        return True  

    def adjust_cwnd(self, ack_received):
        if ack_received:
            if self.cwnd < self.ssthresh:
          
                self.cwnd += 1
                print(f"Sent packet. cwnd increased to {self.cwnd}. (Slow Start)")
            else:
               
                self.cwnd += 1 / self.cwnd
                print(f"Sent packet. cwnd increased to {self.cwnd:.2f}. (Congestion Avoidance)")
            self.dup_acks = 0
        else:
            if not self.in_fast_recovery:
    
                print(f"Packet lost. Triggering Fast Recovery.")
                self.ssthresh = max(self.cwnd / 2, 1) 
                self.cwnd = self.ssthresh + 3  
                self.in_fast_recovery = True
                print(f"cwnd set to {self.cwnd} (Fast Recovery started).")
            else:
                # In Fast Recovery
                self.dup_acks += 1
                self.cwnd += 1
                print(f"Duplicate ACK received. cwnd increased to {self.cwnd} (Fast Recovery).")
                
            # If three duplicate ACKs are received, exit Fast Recovery
            if self.dup_acks >= 3:
                self.in_fast_recovery = False
                print(f"Exiting Fast Recovery. cwnd reduced to {self.ssthresh}.")

    def simulate(self):
        for _ in range(20): 
            time.sleep(self.baseRTT)  
            ack_received = self.send_packet()
            self.adjust_cwnd(ack_received)


if __name__ == "__main__":
    sender = TCPSender()
    sender.simulate()
