import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import threading
from PIL import Image
import time

# Define the nodes and edges based on your updated topology description
nodes = ['client', 'A', 'B', 'C', 'D', 'E', 'Server']

edges = [
    ('client', 'A'),
    ('client', 'C'),
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'D'),
    ('D', 'C'),
    ('B', 'E'),
    ('C', 'E'),
    ('B', 'Server'),
    ('E', 'Server')
]

# Manually define the positions of each node to avoid overlapping
pos = {
    'client': (0, 2),
    'A': (1, 3),
    'B': (3, 3),
    'C': (1, 1),
    'D': (2, 2),
    'E': (3, 1),
    'Server': (4, 2)
}

# Create the graph and add nodes and edges
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Create a color map for nodes, making the client blue and the server red
node_colors = ['red' if node == 'Server' else 'blue' for node in G.nodes()]

# Create a label dictionary for better visualization
labels = {node: f"{node}" for node in G.nodes()}

# TCP Connection Parameters
HOST = 'localhost'
PORT = 12346  # Receiving from the intermediate nodes

client_times = {}  # Dictionary to store client times
client_count = 0  # Client count starts from 0

# Names for the clients
client_names = ["MSACK", "MAIMD", "Cubic", "Proposed approach"]

# TCP server function (simulate server behavior)
def start_server(image_name):
    global client_count
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT} for {image_name}...")

    while client_count < 4:  # Limit the number of clients to 4
        print("Waiting for a new client connection...")
        connection, client_address = server_socket.accept()
        client_count += 1
        client_name = client_names[client_count - 1]
        print(f"Connection from {client_address} established as {client_name}.")

        start_time = time.time()
        total_bytes = 0

        try:
            with open(image_name, 'wb') as image_file:
                while True:
                    data = connection.recv(512)
                    if not data:
                        break
                    image_file.write(data)
                    total_bytes += len(data)
                    print(f"Received {len(data)} bytes, total so far: {total_bytes} bytes")

            print(f"Image {image_name} received successfully.")

        except Exception as e:
            print(f"Error while receiving the image: {e}")

        finally:
            connection.close()
            print(f"Connection with {client_name} closed.")

            # Calculate time taken for the client and store it in the dictionary
            elapsed_time = time.time() - start_time
            client_times[client_name] = elapsed_time
            print(f"{client_name} completed in {elapsed_time:.2f}s")

            # Break the loop if we've reached 4 clients
            if client_count >= 4:
                break

    server_socket.close()

    # Open the image after all clients are done
    try:
        img = Image.open(image_name)
        img.show()
        print(f"Image {image_name} opened successfully.")
    except Exception as e:
        print(f"Error opening the image: {e}")

# Visualization with Matplotlib
fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Create 4 subplots (2x2)

# Define the flow path
flow_path = [
    ('client', 'A'),
    ('A', 'B'),
    ('B', 'D'),
    ('D', 'C'),
    ('C', 'E'),
    ('E', 'Server')
]

# Visualization function (won't run until all clients are processed)
def visualize():
    for i, ax in enumerate(axes.flat):
        client_name = client_names[i]  # Use the custom names for clients
        if client_name in client_times:
            total_time = client_times[client_name]  # Use time for each client
            print(f"Opening animation for {client_name} with total time {total_time:.2f}s")

            # Create a new figure for each client
            fig, ax = plt.subplots(figsize=(8, 6))

            # Time per frame for the client's animation
            frame_interval = total_time / len(flow_path)  # Time per frame
            elapsed_time = 0  # Time elapsed during animation

            # Function to simulate message flow and update time
            def simulate_message_flow(frame, ax, flow_path):
                ax.text(3.5, 5, f"Total Time: {total_time:.2f}s", fontsize=12, color="black", verticalalignment="center")
                global elapsed_time
                elapsed_time = frame * frame_interval  # Update elapsed time

                # Show progressively increasing edges (moving dotted line effect)
                current_path = flow_path[:frame]  # Increase the path by one edge per frame

                # Redraw the graph with the path showing in dotted lines
                nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, edge_color='black', node_size=2000, font_size=12, ax=ax)

                # Draw the dotted edges for the flow path
                if current_path:
                    nx.draw_networkx_edges(G, pos, edgelist=current_path, edge_color='red', style='dotted', width=5, ax=ax)

                # Display elapsed time on the side of the graph
                ax.text(3.5, 3, f"Elapsed Time: {elapsed_time:.2f}s", fontsize=12, color="black", verticalalignment="center")

                # Set title and update frame number
                ax.set_title(f"{client_name} - Network Topology")

            # Function to update the graph in each frame (for animation)
            def update_frame(i):
                ax.clear()
                simulate_message_flow(i, ax, flow_path)

            # Create the animation for each client's separate window
            ani = FuncAnimation(fig, update_frame, frames=len(flow_path) + 1, interval=frame_interval * 1000, repeat=True)

            # Show the plot with the animation for this client
            plt.show()

            # Wait for the animation to finish before proceeding to the next client
            print(f"Finished animation for {client_name}")

    # Now that all animations are done, display the times and names in a graph
    display_client_times_graph()

# Function to display the bar chart for client times
def display_client_times_graph():
    # Create a bar chart of client names vs their times
    clients = list(client_times.keys())
    times = list(client_times.values())

    plt.figure(figsize=(8, 6))
    plt.bar(clients, times, color='skyblue')
    plt.xlabel('Clients')
    plt.ylabel('Completion Time (seconds)')
    plt.title('Client Completion Times')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Run the server and collect client times
start_server('received_image.jpg')

# After all clients have connected, display the times and the animation
print("Client Completion Times:")
for client, time_taken in client_times.items():
    print(f"{client}: {time_taken:.2f}s")

# Now that all clients are processed, run the visualization
visualize()
