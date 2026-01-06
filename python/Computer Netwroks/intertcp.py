import socket
import time

def forward_data(from_socket, to_socket):
    # Receive data from the previous node
    data = from_socket.recv(1024)
    print(f"Relaying data: {data.decode()}")  # Debug: check what data is being relayed

    # Send data to the next node
    to_socket.send(data)
    print(f"Data sent to the next node.")  # Debug: confirm data was sent to next node

def start_intermediate_node(port, next_node_host, next_node_port):
    # Create a socket for this intermediate node
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))  # Listening on the given port
    server_socket.listen(1)

    print(f"Intermediate Node listening on port {port}...")

    # Accept connection from the previous node
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Connect to the next node
    next_node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    next_node_socket.connect((next_node_host, next_node_port))
    print(f"Connected to the next node at {next_node_host}:{next_node_port}")

    # Forward the data to the next node
    forward_data(client_socket, next_node_socket)
    time.sleep(2)
    # Close the connections
    client_socket.close()
    next_node_socket.close()
    server_socket.close()

if __name__ == "__main__":
    # Start each intermediate node in sequence:
    # Node 1 forwards to Node 2
    start_intermediate_node(12345, 'localhost', 12346)

