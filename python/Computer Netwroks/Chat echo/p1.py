import socket

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("localhost",12345))
print("Server Listening")
ss.listen(1)
while 1:
    cs,add=ss.accept()
    msg=cs.recv(1024)
    print("Client:",msg.decode())
    m=input("Server:")
    cs.send(m.encode())
    cs.close()  