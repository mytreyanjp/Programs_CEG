import socket
import random


def selective_repeat_server(host='localhost', port=8080, frame_count=10, window_size=4):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server is running on {host}:{port}")

    # To track received frames in the current window
    received_frames = [False] * frame_count
    expected_frame = 0

    while True:
        data, client_address = server_socket.recvfrom(1024)
        frame = int(data.decode())

        # Simulate frame loss
        if random.random() > 0.3:  # 70% chance to receive the frame
            if frame >= expected_frame and frame < expected_frame + window_size:
                print(f"Received frame {frame}")

                if not received_frames[frame]:  # Frame is received for the first time
                    received_frames[frame] = True
                    print(f"Acknowledging frame {frame}")
                    server_socket.sendto(str(frame).encode(), client_address)

                # Move the window if the expected frame has been received
                while expected_frame < frame_count and received_frames[expected_frame]:
                    expected_frame += 1
            else:
                print(f"Discarded frame {frame}, outside of window [{expected_frame}-{expected_frame + window_size - 1}]")
        else:
            print(f"Frame {frame} lost (simulated)")

        # Check if all frames have been received
        if expected_frame >= frame_count:
            break

    print("All frames received successfully.")
    server_socket.close()

selective_repeat_server()
