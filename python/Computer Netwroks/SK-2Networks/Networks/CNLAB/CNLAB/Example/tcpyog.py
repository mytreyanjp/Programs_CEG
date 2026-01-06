import socket

def tcp_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"TCP server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                hostname = conn.recv(1024).decode()
                if not hostname:
                    break
                
                # Determine IP address based on hostname
                if hostname == "google":
                    ip_address = "10.11.2.4"
                elif hostname == "yahoo":
                    ip_address = "128.36.96.3"
                else:
                    ip_address = "Hostname not found"

                conn.sendall(ip_address.encode())

if __name__ == "__main__":
    tcp_server()
