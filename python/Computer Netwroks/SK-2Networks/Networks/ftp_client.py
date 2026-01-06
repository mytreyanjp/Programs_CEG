import socket
import os

HOST = '127.0.0.1'
PORT = 2121

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Connected to server {HOST}:{PORT}")

def send_command(command):
    client.send(command.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)

def get_file(file_name):
    client.send(f"GET {file_name}".encode('utf-8'))
    with open(file_name, 'wb') as f:
        while True:
            data = client.recv(1024)
            if not data:
                break
            f.write(data)
    print(f"File {file_name} downloaded successfully.")

def put_file(file_name):
    if os.path.isfile(file_name):
        client.send(f"PUT {file_name}".encode('utf-8'))
        with open(file_name, 'rb') as f:
            client.sendfile(f)
        print(f"File {file_name} uploaded successfully.")
    else:
        print(f"File {file_name} does not exist.")

while True:
    command = input("Enter command (LIST, GET <filename>, PUT <filename>, CD <directory>): ")
    command_parts = command.split()

    if len(command_parts) < 1:
        continue

    cmd = command_parts[0].upper()

    if cmd == "LIST":
        send_command("LIST")

    elif cmd == "CD" and len(command_parts) > 1:
        send_command(f"CD {command_parts[1]}")

    elif cmd == "GET" and len(command_parts) > 1:
        get_file(command_parts[1])

    elif cmd == "PUT" and len(command_parts) > 1:
        put_file(command_parts[1])

    elif cmd == "EXIT":
        client.close()
        print("Disconnected from server.")
        break

    else:
        print("Invalid command.")
