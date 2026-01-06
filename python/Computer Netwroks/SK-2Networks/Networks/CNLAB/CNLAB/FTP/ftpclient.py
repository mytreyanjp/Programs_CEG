import socket
SERVER_ADDRESS = '127.0.0.1'  # Localhost
PORT = 8080
BUFFER_SIZE = 1024
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((SERVER_ADDRESS, PORT))
            print("Connected to server.")
        except ConnectionError:
            print("Connection failed.")
            return
        try:
            with open("rea.txt", "rb") as file:
                print("Sending file...")

                # Read data in chunks and send to the server
                while (chunk := file.read(BUFFER_SIZE)):
                    bytes_sent = client_socket.send(chunk)
                    if bytes_sent == 0:
                        print("Connection closed by server.")
                        break
                    print(f"Sent {bytes_sent} bytes")
            
            print("File sent successfully.")
            
        except OSError as e:
             print(f"Error: {e}")

if __name__ == "__main__":
    main()
