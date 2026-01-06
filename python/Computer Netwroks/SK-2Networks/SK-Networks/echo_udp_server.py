from socket import *

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("UDP server is running")

while True:
    message, clientAddress = serverSocket.recvfrom(1024)
    print("Received message from:", clientAddress)
    
    message = f"ECHO: {message.decode()}"
    print(message)
    
    serverSocket.sendto(message.encode(), clientAddress)
