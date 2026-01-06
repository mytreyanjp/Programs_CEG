import socket

cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect(("localhost",12345))
while 1:
    msg=input("Client:")
    cs.send(msg.encode())
    m=cs.recv(1024)
    print("Server:",m.decode())
    cs.close()