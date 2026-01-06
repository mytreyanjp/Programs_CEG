from socket import *

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1025    

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(f"SMTP server is running on {SERVER_HOST}:{SERVER_PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    client_socket.send(b"220 SMTP Server Ready\r\n")

    while True:

        client_data = client_socket.recv(1024).decode()
        print(f"Client: {client_data}")

        if client_data.startswith("HELO"):
            client_socket.send(b"250 Hello, pleased to meet you\r\n")


        elif client_data.startswith("MAIL FROM"):
            client_socket.send(b"250 OK\r\n")


        elif client_data.startswith("RCPT TO"):
            client_socket.send(b"250 OK\r\n")


        elif client_data.startswith("DATA"):
            client_socket.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
            data = client_socket.recv(1024).decode()
            print(f"Email data: {data.strip()}")
            client_socket.send(b"250 OK, message accepted\r\n")

            
        elif client_data.startswith("QUIT"):
            client_socket.send(b"221 Bye\r\n")
            break
        else:
            client_socket.send(b"500 Syntax error, command unrecognized\r\n")

    client_socket.close()
