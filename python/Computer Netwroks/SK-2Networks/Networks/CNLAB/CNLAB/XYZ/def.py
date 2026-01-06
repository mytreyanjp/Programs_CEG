from socket import*
serverport=1234
server=socket(AF_INET,SOCK_DGRAM)
server.bind(('',serverport))
print("server is ready to receive")
a=["sow","gv"]
z=len(a)
pos=-1
while True:
    conn,addr=server.recvfrom(2048)
    f=conn.decode()
    for x in range(0,z):
        if a[x]==f:
            pos=x
            break
    server.sendto(str(pos).encode(),addr)
    