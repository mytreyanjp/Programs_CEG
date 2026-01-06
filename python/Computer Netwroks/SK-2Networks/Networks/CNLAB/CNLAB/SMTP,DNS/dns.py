import socket

def dns_query(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"The IP address of {domain} is {ip_address}")
    except socket.gaierror:
        print(f"Failed to resolve {domain}")

dns_query("www.google.com")

