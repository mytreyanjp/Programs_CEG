import random
import time

class GoBackNProtocol:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = 0
        self.acknowledged_frames = 0
        self.frames = list(range(total_frames))

    def send_frame(self, frame):
        print(f"Sending frame {frame}")
        if random.random() < 0.2:
            print(f"Frame {frame} lost!")
            return False
        return True

    def receive_ack(self, ack):
        print(f"Received ACK for frame {ack}")
        self.acknowledged_frames = ack + 1

    def run(self):
        while self.acknowledged_frames < self.total_frames:
            while (self.sent_frames < self.total_frames and 
                   self.sent_frames - self.acknowledged_frames < self.window_size):
                if not self.send_frame(self.sent_frames):
                    break
                self.sent_frames += 1
            
            for i in range(self.acknowledged_frames, self.sent_frames):
                self.receive_ack(i)

            if self.sent_frames > self.acknowledged_frames:
                self.sent_frames = self.acknowledged_frames

            time.sleep(1)

        print("All frames successfully sent and acknowledged!")

WINDOW_SIZE = 4
TOTAL_FRAMES = 20

gbn = GoBackNProtocol(WINDOW_SIZE, TOTAL_FRAMES)
gbn.run()
