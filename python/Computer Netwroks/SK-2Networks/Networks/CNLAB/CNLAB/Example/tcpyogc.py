import socket

def tcp_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        hostname = input("Enter hostname to resolve (e.g., google or yahoo): ")
        client_socket.sendall(hostname.encode())
        ip_address = client_socket.recv(1024).decode()
        print(f"IP address for {hostname}: {ip_address}")

if __name__ == "__main__":
    tcp_client()
