from socket import*
serverPort=10025
serverName="localhost"
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sen=input("Input lowercase")
clientSocket.send(sen.encode())
mod=clientSocket.recv(1024)
print("From server:",mod.decode())
clientSocket.close()