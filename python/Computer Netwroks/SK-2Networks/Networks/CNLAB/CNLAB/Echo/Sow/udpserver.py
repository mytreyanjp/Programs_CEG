# server_udp_echo.py
import socket

def start_server_udp_echo(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Echo Server listening on {host}:{port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            server_socket.sendto(data, addr)  # Echo the message back

if __name__ == "__main__":
    start_server_udp_echo()

