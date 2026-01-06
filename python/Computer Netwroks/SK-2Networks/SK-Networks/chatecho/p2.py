import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("Server:", msg)
            else:
                break
        except:
            print("An error occurred while receiving a message.")
            break

def send_messages(sock):
    while True:
        cmsg = input("Client: ")
        sock.send(cmsg.encode())

# Create a socket and connect to the server
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(("localhost", 8080))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(cs,))
receive_thread.start()

# Start sending messages to the server
send_messages(cs)

# Close the socket when done
cs.close()