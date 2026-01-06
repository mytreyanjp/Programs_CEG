from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while 1:
    sentence = input().encode()
    clientSocket.send(sentence)
    message = clientSocket.recv(1024)
    print(message)
clientSocket.close()