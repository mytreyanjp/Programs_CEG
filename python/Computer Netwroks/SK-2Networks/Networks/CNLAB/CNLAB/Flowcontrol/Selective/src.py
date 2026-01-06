import socket
import time

def selective_repeat_client(host='localhost', port=8080, frame_count=10, window_size=4):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)  # Set a timeout for retransmissions

    base = 0
    next_frame = 0
    sent_frames = [False] * frame_count  # Track whether each frame has been sent
    ack_received = [False] * frame_count  # Track whether each frame has been acknowledged

    while base < frame_count:
        # Send frames within the window
        while next_frame < base + window_size and next_frame < frame_count:
            if not sent_frames[next_frame]:  # Send the frame if it hasn't been sent
                print(f"Sending frame {next_frame}")
                client_socket.sendto(str(next_frame).encode(), (host, port))
                sent_frames[next_frame] = True  # Mark frame as sent
            next_frame += 1
            time.sleep(0.5)  # Delay to simulate transmission time

        # Wait for acknowledgments
        try:
            ack, _ = client_socket.recvfrom(1024)
            ack = int(ack.decode())
            print(f"Acknowledgment received for frame {ack}")
            ack_received[ack] = True  # Mark frame as acknowledged

            # Slide the window when base frame is acknowledged
            while base < frame_count and ack_received[base]:
                base += 1

            # Reset `next_frame` to ensure the window advances only with unacknowledged frames
            next_frame = base

        except socket.timeout:
            print("Timeout, resending unacknowledged frames in window...")
            # Resend frames that haven't been acknowledged within the window
            next_frame = base  # Set `next_frame` to the base to resend frames in the window
            for i in range(base, base + window_size):
                if i < frame_count and not ack_received[i]:  # Only resend unacknowledged frames
                    print(f"Resending frame {i}")
                    client_socket.sendto(str(i).encode(), (host, port))
                    time.sleep(0.5)  # Delay to simulate retransmission time

    print("All frames sent and acknowledged successfully.")
    client_socket.close()

selective_repeat_client()
