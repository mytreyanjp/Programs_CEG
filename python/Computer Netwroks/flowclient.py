import time
import random

def send_frame(frame_number):
    print(f"Sending Frame {frame_number}")
    return random.choice([True, False]) 

def sliding_window(window_size):
    frame_number = 1
    total_frames = 10
    unacked_frames = {}

    while frame_number <= total_frames or unacked_frames:
        # Send frames within the current window
        while frame_number <= total_frames and len(unacked_frames) < window_size:
            success = send_frame(frame_number)
            if success:
                print(f"ACK received for Frame {frame_number}")
            else:
                print(f"Error for Frame {frame_number}, resending later...")
                unacked_frames[frame_number] = False 
            frame_number += 1
            time.sleep(1) 

      
        for unacked in list(unacked_frames):
            success = send_frame(unacked)
            if success:
                print(f"ACK received for Frame {unacked}")
                del unacked_frames[unacked] 
            else:
                print(f"Error for Frame {unacked}, resending...")

        time.sleep(1) 

sliding_window(3)  

