from socket import *

serversocket = socket(AF_INET,SOCK_STREAM)
serveraddress = ('localhost', 8081)
serversocket.bind(serveraddress)
serversocket.listen(1)

while True:
    client, clientaddress = serversocket.accept()
    try:
        message = client.recv(1024)
        html_content = """
        <html>
        <head>
        <title> Salai Kowshikan's server </title>
        </head>
        <body>
        <h1> Welcome to Salai Kowshikan's server </h1>
        </body>
        </html>
        """
        
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html_content)}\n\n{html_content}"
        client.sendall(response.encode())
    finally:
        client.close()