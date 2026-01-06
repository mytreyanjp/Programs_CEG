import socket

# Server setup: TCP socket and UDP socket
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding TCP and UDP sockets to the same port (for simplicity)
host = "127.0.0.1"
port = 12345
tcp_server.bind((host, port))
tcp_server.listen(1)
print(f"Server listening on {host}:{port}")

# Accept TCP connections
tcp_conn, tcp_addr = tcp_server.accept()
print(f"TCP connection established with {tcp_addr}")

# Receive TCP packets
while True:
    data = tcp_conn.recv(1024)
    if not data:
        break
    print(f"TCP packet received: {data.decode()}")
    tcp_conn.send(b"ACK")  # Send acknowledgment

# UDP receive loop
print("Switching to UDP mode...")
while True:
    data, udp_addr = udp_server.recvfrom(1024)
    if not data:
        break
    print(f"UDP packet received from {udp_addr}: {data.decode()}")

tcp_conn.close()
tcp_server.close()
udp_server.close()
print("Server connection closed.")
