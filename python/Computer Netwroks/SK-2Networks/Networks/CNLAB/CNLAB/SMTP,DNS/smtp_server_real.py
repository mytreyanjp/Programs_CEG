import socket
import threading

HOST = '127.0.0.1'  # Localhost
PORT = 2525         # Non-standard SMTP port for testing

def handle_client(client_socket):
    # Send a 220 (Service Ready) message to the client
    client_socket.send(b"220 SMTP Server Ready\r\n")
    
    from_address = None
    to_address = None
    data_mode = False
    message = []

    while True:
        # Receive data from client
        data = client_socket.recv(1024).decode('utf-8').strip()
        if not data:
            break

        print("Received:", data)

        # Process the SMTP commands
        if data.startswith("MAIL FROM:"):
            from_address = data.split(":")[1].strip()
            client_socket.send(b"250 OK\r\n")

        elif data.startswith("RCPT TO:"):
            to_address = data.split(":")[1].strip()
            client_socket.send(b"250 OK\r\n")

        elif data == "DATA":
            data_mode = True
            client_socket.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")

        elif data == "." and data_mode:
            data_mode = False
            # Print received email details to simulate sending
            print("\n--- Email Received ---")
            print(f"From: {from_address}")
            print(f"To: {to_address}")
            print("Message:")
            print("\n".join(message))
            print("---------------------\n")
            client_socket.send(b"250 OK Message received\r\n")
            message = []  # Reset for new message

        elif data_mode:
            message.append(data)

        elif data == "QUIT":
            client_socket.send(b"221 Bye\r\n")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"SMTP Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

