from socket import*
ser='localhost'
serport=12000
cli=socket(AF_INET,SOCK_DGRAM)
msg=input("Input lowercase sentence")
cli.sendto(msg.encode(),(ser,serport))
mod,seraddr=cli.recvfrom(2048)
print(mod.decode())
cli.close()