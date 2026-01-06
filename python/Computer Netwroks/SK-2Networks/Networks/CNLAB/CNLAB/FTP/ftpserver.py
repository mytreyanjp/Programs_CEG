import socket
HOST = '127.0.0.1'  # Localhost
PORT = 8080
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(3)
    print(f"Server listening on {HOST}:{PORT}...")

    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Open a file to write received data
        with open("sam.txt", "wb") as file:
            print("Receiving file...")

            # Receive data in chunks and write to the file
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
                print(f"Received {len(data)} bytes")

        print("File received successfully")
