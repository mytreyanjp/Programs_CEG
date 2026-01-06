from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = json.loads(post_data.decode('utf-8')).get('message', '')

        # Convert the message to uppercase
        uppercase_message = message.upper()

        response = f"Message received: {uppercase_message}"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    server_address = ('localhost', 5000)  # Listens on all network interfaces
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 5000...")
    httpd.serve_forever()







