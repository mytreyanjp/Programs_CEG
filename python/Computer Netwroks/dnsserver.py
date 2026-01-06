import socket

def start_dns_server(host='127.0.0.1', port=5300):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"DNS Server is running on {host}:{port}")

        while True:
            try:
                # Receive a request
                message, client_address = server_socket.recvfrom(1024)
                hostname = message.decode('utf-8')

                try:
                    # Resolve the hostname to an IP address
                    ip_address = socket.gethostbyname(hostname)
                except socket.gaierror:
                    # Handle the case where the hostname could not be resolved
                    ip_address = '0.0.0.0'

                # Send the IP address back to the client
                server_socket.sendto(ip_address.encode('utf-8'), client_address)
            except KeyboardInterrupt:
                print("Server shutting down.")
                break

if __name__ == "__main__":
    start_dns_server()
