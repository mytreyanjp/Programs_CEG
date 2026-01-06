import socket

def udp_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP server listening on {host}:{port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            hostname = data.decode()
            print(f"Received '{hostname}' from {addr}")
            
            # Determine IP address based on hostname
            if hostname == "google":
                ip_address = "10.11.2.4"
            elif hostname == "yahoo":
                ip_address = "128.36.96.3"
            else:
                ip_address = "Hostname not found"

            server_socket.sendto(ip_address.encode(), addr)

if __name__ == "__main__":
    udp_server()
