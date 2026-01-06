import socket

HOST = '127.0.0.1'  # Server address
PORT = 2525         # Server port

def send_email(from_email, to_email, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Read the server's response
    print(client.recv(1024).decode('utf-8'))

    # Send MAIL FROM command
    client.send(f"MAIL FROM: {from_email}\r\n".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    # Send RCPT TO command
    client.send(f"RCPT TO: {to_email}\r\n".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    # Send DATA command
    client.send("DATA\r\n".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    # Send the message body
    for line in message.splitlines():
        client.send(f"{line}\r\n".encode('utf-8'))

    # End message data with a single period
    client.send(".\r\n".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    # Send QUIT command
    client.send("QUIT\r\n".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    client.close()

if __name__ == "__main__":
    from_email = "hariharan09092004@gmail.com"
    to_email = "speed09092004@gmail.com"
    message = """Subject: Test Email

    This is a test message from the SMTP client.
    """
    send_email(from_email, to_email, message)

