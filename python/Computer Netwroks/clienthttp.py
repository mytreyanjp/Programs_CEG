import http.client
import json

server_ip = 'localhost'  # Server's IP address
port = 5000

conn = http.client.HTTPConnection(server_ip, port)

# Input your message in lowercase
message_text = input("Enter your message in lowercase: ")
message = {'message': message_text}
headers = {'Content-type': 'application/json'}
json_data = json.dumps(message)

conn.request("POST", "/message", json_data, headers)
response = conn.getresponse()
print("Server response- Upper case:", response.read().decode())
conn.close()
