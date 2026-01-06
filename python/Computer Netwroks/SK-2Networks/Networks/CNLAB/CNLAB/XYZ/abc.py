from socket import*
serverport=1234
servername="localhost"
clientsocket=socket(AF_INET,SOCK_DGRAM)
msg=input("enter")
clientsocket.sendto(msg.encode(),(servername,serverport))
mod=clientsocket.recv(1024).decode()
print(f"response:{mod}")
clientsocket.close()