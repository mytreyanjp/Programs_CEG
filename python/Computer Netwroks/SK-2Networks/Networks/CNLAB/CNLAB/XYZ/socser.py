from socket import*
serport=12000
serSocket=socket(AF_INET,SOCK_DGRAM)
serSocket.bind(('',serport))
print("The server is ready to receive")
while 1:
    msg,cli=serSocket.recvfrom(2048)
    mod=msg.upper()
    serSocket.sendto(mod,cli)