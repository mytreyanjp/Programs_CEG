from socket import*
serverPort=10025
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while 1:
    conn,addr=serverSocket.accept()
    sen=conn.recv(1024)
    cap=sen.upper()
    conn.send(cap)
    conn.close()