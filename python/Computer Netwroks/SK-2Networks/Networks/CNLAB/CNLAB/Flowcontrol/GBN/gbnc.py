import socket
import time

def go_back_n_client(host='localhost', port=8080, window_size=4, frame_count=10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    base = 0
    next_frame = 0

    while base < frame_count:
        # Send frames within the window size
        while next_frame < base + window_size and next_frame < frame_count:
            print(f"Sending frame {next_frame}")
            client_socket.sendto(str(next_frame).encode(), (host, port))
            next_frame += 1
            time.sleep(1)  # Delay to simulate sending time

        try:
            # Wait for an acknowledgment
            ack, _ = client_socket.recvfrom(1024)
            ack = int(ack.decode())
            print(f"Received acknowledgment for frame {ack}")

            # Slide the window based on the acknowledged frame
            base = ack + 1

        except socket.timeout:
            # Timeout occurred, reset `next_frame` to `base` to resend frames
            print("Timeout! Resending frames...")
            next_frame = base

    print("All frames sent successfully.")
    client_socket.close()

go_back_n_client()
