import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8081)
server_socket.bind(server_address)


server_socket.listen(1)
print("Server listening on port 8081")

while True:
    connection, client_address = server_socket.accept()
    try:
        request_data = connection.recv(1024)
        try:
            request = request_data.decode('utf-8')
        except UnicodeDecodeError:
            request = "Unable to decode request"

        print("Received request:", request)
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Salai Kowshikan's server</title>
        </head>
        <body>
            <h1>Hello from Salai Kowshikan!</h1>
            <p>Welcome to the downtown</p>
        </body>
        </html>
        """
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
        connection.sendall(response.encode('utf-8'))
    finally:
        connection.close()

