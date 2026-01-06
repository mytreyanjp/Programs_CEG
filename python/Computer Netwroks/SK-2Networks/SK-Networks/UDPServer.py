from socket import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(("",serverPort))
print("The server is listening")

def login(password):
    if password == "pipopipopopipo".encode():
        return "Login successful!"
    else:
        return "Liar, wrong password"

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = login(message).encode()
    serverSocket.sendto(modifiedMessage,clientAddress)
    
