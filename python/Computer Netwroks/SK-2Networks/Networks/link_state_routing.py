import heapq

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0 

    priority_queue = [(0, start_node)]
    visited = set()
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes

def reconstruct_path(previous_nodes, start_node, target_node):
    path = []
    current_node = target_node
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()
    return path if path[0] == start_node else None

graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'C': 3, 'D': 4},
    'C': {'A': 5, 'B': 3, 'D': 2, 'E': 3},
    'D': {'B': 4, 'C': 2, 'E': 1},
    'E': {'C': 3, 'D': 1}
}

start_node = 'A'

distances, previous_nodes = dijkstra(graph, start_node)

print(f"Shortest distances from node {start_node}:")
for node, distance in distances.items():
    print(f"  {start_node} -> {node} : {distance}")

print("\nPaths from start node to each node:")
for target_node in graph:
    if target_node != start_node:
        path = reconstruct_path(previous_nodes, start_node, target_node)
        print(f"  {start_node} -> {target_node} : {' -> '.join(path)}")
