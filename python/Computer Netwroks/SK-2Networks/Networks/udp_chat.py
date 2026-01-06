from socket import *

serverport = 12000
servername = "localhost"
serversocket = socket(AF_INET,SOCK_DGRAM)

while True:
    message = input().encode()
    serversocket.sendto(message,(servername,serverport))
    reply, serveraddress = serversocket.recvfrom(2048)
    print(reply.decode())