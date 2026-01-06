from socket import * 
serverPort = 12001
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("I am running")

while 1:
    connectionSocket, address = serverSocket.accept()
    print("Connection accepted from: ",address)
    while 1:
        sentence = connectionSocket.recv(1024)
        print(sentence)
        message = input().encode()
        connectionSocket.send(message)
    connectionSocket.close()
    
