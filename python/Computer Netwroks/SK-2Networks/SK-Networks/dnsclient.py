import socket

def query_dns_server(hostname, server_host='127.0.0.1', server_port=5300):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        
        client_socket.sendto(hostname.encode('utf-8'), (server_host, server_port))

        
        ip_address, _ = client_socket.recvfrom(1024)
        return ip_address.decode('utf-8')

if __name__ == "__main__":
    hostname = input("Enter hostname to query: ")
    ip_address = query_dns_server(hostname)
    print(f"IP address for {hostname} is {ip_address}")
