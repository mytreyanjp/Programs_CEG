import time
import random

class StopAndWait:
    def __init__(self):
        self.frame_number = 0
        self.ack_received = True

    def send_frame(self):
        print(f"Sending frame {self.frame_number}")
        success = random.choices([True, False], weights=[80, 20], k=1)[0]
        return success

    def wait_for_ack(self):
        timeout = 2
        time.sleep(random.uniform(0.5, 2))
        ack_received = random.choices([True, False], weights=[80, 20], k=1)[0]
        return ack_received

    def start(self, total_frames=5):
        sent_frames = 0
        while sent_frames < total_frames:
            if self.ack_received:
                success = self.send_frame()
                if success:
                    print(f"Frame {self.frame_number} sent successfully.")
                    self.ack_received = self.wait_for_ack()
                    if self.ack_received:
                        print(f"ACK for frame {self.frame_number} received.")
                        self.frame_number += 1
                        sent_frames += 1
                    else:
                        print(f"ACK for frame {self.frame_number} lost. Resending frame.")
                else:
                    print(f"Frame {self.frame_number} lost during transmission. Resending frame.")
            else:
                print(f"Resending frame {self.frame_number} due to lost ACK.")
                self.ack_received = self.wait_for_ack()
                if self.ack_received:
                    print(f"ACK for frame {self.frame_number} received after retransmission.")
                    self.frame_number += 1
                    sent_frames += 1
                else:
                    print(f"ACK for frame {self.frame_number} still lost. Retrying...")

stop_and_wait = StopAndWait()
stop_and_wait.start(total_frames=5)
