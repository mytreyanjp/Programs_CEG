import socket

def start_udp_echo_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Echo Server listening on {host}:{port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received {data.decode()} from {addr}")
            server_socket.sendto(data, addr)

if __name__ == "__main__":
    start_udp_echo_server()
