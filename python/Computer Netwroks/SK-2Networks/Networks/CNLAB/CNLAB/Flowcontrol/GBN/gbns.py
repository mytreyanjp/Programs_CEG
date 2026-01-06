import socket
import time
import random

def go_back_n_server(host='localhost', port=8080, frame_count=10):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server is running on {host}:{port}")

    expected_frame = 0

    while True:
        data, client_address = server_socket.recvfrom(1024)
        frame = int(data.decode())

        # Simulate frame loss with 50% probability
        if random.random() > 0.5:
            print(f"Received frame {frame}")
            if frame == expected_frame:
                # Delay acknowledgment for a specific frame (simulate network delay)
                if expected_frame == 2:
                    print("Delaying acknowledgment")
                    time.sleep(5)

                print(f"Acknowledging frame {frame}")
                server_socket.sendto(str(frame).encode(), client_address)
                expected_frame += 1
            else:
                print(f"Discarded frame {frame}, expecting frame {expected_frame}")
        else:
            print(f"Frame lost: {frame}")

        # Stop when all frames are received and acknowledged
        if expected_frame >= frame_count:
            break

    print("All frames received successfully.")
    server_socket.close()

go_back_n_server()
