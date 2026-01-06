import socket

def stop_and_wait_server(port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)  # Listen for incoming connections
    print("Server is waiting for connections...")

    conn, addr = server_socket.accept()  # Accept a single connection
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break  # Break if there's no data (client disconnected)
        
        print(f"Received: {data.decode()}")
        
        # Send acknowledgment
        ack = f"ACK {data.decode()}"
        conn.sendall(ack.encode())
        print(f"Sent: {ack}")

    conn.close()  # Close the connection when done
    print("Connection closed")

# Start the server
stop_and_wait_server(12345)
