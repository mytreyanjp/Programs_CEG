import socket
import os
import threading

HOST = '127.0.0.1'
PORT = 2121

def handle_client(client_socket):
    current_directory = os.getcwd()
    
    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            
            command_parts = command.split()
            if len(command_parts) < 1:
                continue

            cmd = command_parts[0].upper()

            if cmd == "LIST":
                files = os.listdir(current_directory)
                if not files:
                    response = "The directory is empty"
                else:
                    response = "\n".join(files)
                client_socket.send(response.encode('utf-8'))

            elif cmd == "CD" and len(command_parts) > 1:
                directory = command_parts[1]
                try:
                    os.chdir(directory)
                    current_directory = os.getcwd()
                    client_socket.send(f"Changed directory to {current_directory}".encode('utf-8'))
                except FileNotFoundError:
                    client_socket.send(f"Directory not found: {directory}".encode('utf-8'))

            elif cmd == "GET" and len(command_parts) > 1:
                file_name = command_parts[1]
                file_path = os.path.join(current_directory, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    client_socket.send(data)
                else:
                    client_socket.send(f"File not found: {file_name}".encode('utf-8'))

            elif cmd == "PUT" and len(command_parts) > 1:
                file_name = command_parts[1]
                file_path = os.path.join(current_directory, file_name)
                with open(file_path, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                client_socket.send(f"File {file_name} received successfully.".encode('utf-8'))

            else:
                client_socket.send("Invalid command.".encode('utf-8'))

        except Exception as e:
            client_socket.send(f"Error: {str(e)}".encode('utf-8'))
            break

    client_socket.close()
    print(f"[DISCONNECTED] Client disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"[NEW CONNECTION] {client_address} connected.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
