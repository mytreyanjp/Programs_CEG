import time
import random

class SlidingWindow:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = 0
        self.ack_received = [False] * total_frames
        self.base = 0 
        self.next_frame = 0

    def send_frame(self, frame_number):
        print(f"Sending frame {frame_number}")
        success = random.choice([True, False])
        return success

    def wait_for_ack(self, frame_number):
        time.sleep(random.uniform(0.5, 2))
        ack_received = random.choice([True, False])
        return ack_received

    def start(self):
        while self.base < self.total_frames:
            while self.next_frame < self.base + self.window_size and self.next_frame < self.total_frames:
                success = self.send_frame(self.next_frame)
                if success:
                    print(f"Frame {self.next_frame} sent successfully.")
                else:
                    print(f"Frame {self.next_frame} lost during transmission.")
                self.next_frame += 1

            for frame_number in range(self.base, min(self.base + self.window_size, self.total_frames)):
                if not self.ack_received[frame_number]:
                    ack_success = self.wait_for_ack(frame_number)
                    if ack_success:
                        print(f"ACK for frame {frame_number} received.")
                        self.ack_received[frame_number] = True
                    else:
                        print(f"ACK for frame {frame_number} lost. Resending frames starting from {frame_number}.")
                        self.next_frame = frame_number
                        break

            while self.base < self.total_frames and self.ack_received[self.base]:
                print(f"Sliding window, base frame {self.base} acknowledged.")
                self.base += 1

window_size = 4
total_frames = 10

sliding_window = SlidingWindow(window_size, total_frames)
sliding_window.start()
