import socket

def udp_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        hostname = input("Enter hostname to resolve (e.g., google or yahoo): ")
        client_socket.sendto(hostname.encode(), (host, port))
        ip_address, _ = client_socket.recvfrom(1024)
        print(f"IP address for {hostname}: {ip_address.decode()}")

if __name__ == "__main__":
    udp_client()
