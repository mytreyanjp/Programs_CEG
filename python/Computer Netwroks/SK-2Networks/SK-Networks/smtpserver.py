import socket
import threading
import re

HOST = ''
PORT = 25

def handle_client(client_socket):
    client_socket.send(b'220 Welcome to the Simple SMTP Server\r\n')

    while True:
        try:
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            print(f"Command received: {command}")

            if command.startswith('HELO'):
                client_socket.send(b'250 Hello\r\n')
            elif command.startswith('MAIL FROM:'):
                client_socket.send(b'250 OK\r\n')
            elif command.startswith('RCPT TO:'):
                client_socket.send(b'250 OK\r\n')
            elif command.startswith('DATA'):
                client_socket.send(b'354 End data with <CR><LF>.<CR><LF>\r\n')
                email_data = []
                while True:
                    line = client_socket.recv(1024).decode()
                    if line == '.':
                        break
                    email_data.append(line)
                client_socket.send(b'250 OK\r\n')
                print("Received email data:")
                print("\n".join(email_data))
            elif command.startswith('QUIT'):
                client_socket.send(b'221 Bye\r\n')
                break
            else:
                client_socket.send(b'500 Syntax error, command unrecognized\r\n')
        except Exception as e:
            print(f"Error: {e}")
            client_socket.send(b'500 Internal error\r\n')
            break

    client_socket.close()

def start_smtp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f'SMTP server started on port {PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_smtp_server()
