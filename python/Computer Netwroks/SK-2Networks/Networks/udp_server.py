from socket import *

serverport = 12000
serversocket = socket(AF_INET,SOCK_DGRAM)
serversocket.bind(("",serverport))

while True:
    message, clientaddress = serversocket.recvfrom(2048)
    print(message.decode())
    reply = input().encode()
    serversocket.sendto(reply,clientaddress)