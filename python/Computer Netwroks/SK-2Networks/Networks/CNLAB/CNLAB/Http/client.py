import socket

def fetch_message(host='localhost', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        request = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
        sock.sendall(request)
        
        # Initialize an empty list to collect all response parts
        response = b""
        
        # Keep receiving data until all chunks are received
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk
            
        print(response.decode())

if __name__ == "__main__":
    fetch_message()
