import heapq
 
class LinkStateRouter:
    def __init__(self, graph):
        self.graph = graph  
 
    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]  
        previous_nodes = {node: None for node in self.graph}
 
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
 
            if current_distance > distances[current_node]:
                continue
 
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
 
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
 
        return distances, previous_nodes
 
    def get_path(self, previous_nodes, end):
        path = []
        current_node = end
 
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
 
        path.reverse()
        return path
 
    def get_all_pairs_shortest_paths(self):
        all_pairs_shortest_paths = {}
 
        for node in self.graph:
            distances, previous_nodes = self.dijkstra(node)
            all_pairs_shortest_paths[node] = (distances, previous_nodes)
 
        return all_pairs_shortest_paths
 

if __name__ == "__main__":
    
    graph = {
        'A': {'B': 2, 'C': 5, 'D': 1},
        'B': {'A': 2, 'C': 3, 'E': 4},
        'C': {'A': 5, 'B': 3, 'D': 2, 'F': 1},
        'D': {'A': 1, 'C': 2, 'F': 7, 'G': 3},
        'E': {'B': 4, 'F': 6},
        'F': {'C': 1, 'D': 7, 'E': 6, 'G': 2},
        'G': {'D': 3, 'F': 2},
    }
 
    router = LinkStateRouter(graph)
    all_shortest_paths = router.get_all_pairs_shortest_paths()
 
    for start_node, (distances, previous_nodes) in all_shortest_paths.items():
        print(f"Shortest paths from {start_node}:")
        for end_node in distances:
            if start_node != end_node:
                path = router.get_path(previous_nodes, end_node)
                path_str = " -> ".join(path)
                cost = distances[end_node]
                if len(path) == 2:  
                    print(f"  To {end_node}: Direct link {path_str} with cost {cost}")
                else:  
                    print(f"  To {end_node}: Path {path_str} with cost {cost}")
        print()  
