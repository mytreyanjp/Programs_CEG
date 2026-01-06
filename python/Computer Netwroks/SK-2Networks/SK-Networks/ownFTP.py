import socket
import threading
import os

HOST = ''
PORT = 2122
USER_CREDENTIALS = {"user": "password"}
BASE_DIR = "ftp"

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

class FTPClient:
    def __init__(self):
        self.logged_in = False
        self.username = None

def handle_client(client_socket):
    client_socket.send(b'220 Welcome to the FTP server.\r\n')

    client = FTPClient()
    
    while True:
        command = client_socket.recv(1024).decode().strip()
        if not command:
            break

        print(f"Command received: {command}")
        response = b'500 Command not understood.\r\n'

        if command.startswith('USER'):
            username = command.split()[1]
            if username in USER_CREDENTIALS:
                client.username = username
                response = b'331 User name okay, need password.\r\n'
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('PASS'):
            password = command.split()[1]
            if client.username and USER_CREDENTIALS.get(client.username) == password:
                client.logged_in = True
                response = b'230 User logged in, proceed.\r\n'
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('PWD'):
            if client.logged_in:
                response = f'257 "{BASE_DIR}"\r\n'.encode()
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('LIST'):
            if client.logged_in:
                try:
                    files = '\r\n'.join(os.listdir(BASE_DIR))
                    response = f'150 Here comes the directory listing.\r\n{files}\r\n226 Directory send OK.\r\n'.encode()
                except Exception as e:
                    response = f'550 Failed to list directory.\r\n'.encode()
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('RETR'):
            if client.logged_in:
                filename = command.split()[1]
                try:
                    with open(os.path.join(BASE_DIR, filename), 'rb') as file:
                        data = file.read()
                        response = b'150 Opening data connection.\r\n'
                        client_socket.send(response)
                        client_socket.send(data)
                        response = b'226 Transfer complete.\r\n'
                except FileNotFoundError:
                    response = b'550 File not found.\r\n'
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('STOR'):
            if client.logged_in:
                filename = command.split()[1]
                try:
                    with open(os.path.join(BASE_DIR, filename), 'wb') as file:
                        data = client_socket.recv(1024)
                        while data:
                            file.write(data)
                            data = client_socket.recv(1024)
                    response = b'226 Transfer complete.\r\n'
                except Exception as e:
                    response = b'550 Failed to store file.\r\n'
            else:
                response = b'530 Not logged in.\r\n'

        elif command.startswith('QUIT'):
            response = b'221 Goodbye.\r\n'
            client_socket.send(response)
            break

        client_socket.send(response)

    client_socket.close()

def start_ftp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f'FTP server started on port {PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_ftp_server()
