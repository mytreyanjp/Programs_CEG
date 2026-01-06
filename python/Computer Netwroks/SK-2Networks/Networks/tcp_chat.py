from socket import *

serverport = 12000
servername = "localhost"

clientsocket = socket(AF_INET,SOCK_STREAM)
clientsocket.connect((servername,serverport))

while True:
    message = input().encode()
    clientsocket.send(message)
    sentence = clientsocket.recv(1024).decode()
    print(sentence)
