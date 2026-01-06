import heapq

class Graph:
    def __init__(self):
        self.edges = {}  # Dictionary to store the graph

    def add_edge(self, u, v, cost):
        if u not in self.edges:
            self.edges[u] = []
        if v not in self.edges:
            self.edges[v] = []
        self.edges[u].append((v, cost))
        self.edges[v].append((u, cost))  # Since this is an undirected graph

    def dijkstra(self, start):
        # Priority queue to hold (cost, node)
        pq = []
        heapq.heappush(pq, (0, start))
        distances = {node: float('inf') for node in self.edges}
        distances[start] = 0
        previous_nodes = {node: None for node in self.edges}  # To track next hops
        routing_table = {}  # Store routing table for the start node

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            # Update the routing table
            routing_table[current_node] = (distances[current_node], previous_nodes[current_node])

            for neighbor, weight in self.edges[current_node]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node  # Update next hop
                    heapq.heappush(pq, (distance, neighbor))

        # Construct final routing table
        final_routing_table = {}
        for node in self.edges:
            next_hop = previous_nodes[node] if previous_nodes[node] else node  # Self if no path
            cost = distances[node]
            final_routing_table[node] = (cost, next_hop)

        return final_routing_table


# Example usage
if __name__ == "__main__":
    graph = Graph()
    
    # Adding edges: add_edge(node1, node2, cost)
    graph.add_edge('A', 'B', 1)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('B', 'D', 5)
    graph.add_edge('C', 'D', 1)
    graph.add_edge('D', 'E', 3)

    routers = ['A', 'B', 'C', 'D', 'E']
    
    for router in routers:
        routing_table = graph.dijkstra(router)
        print(f"Routing table for router {router}:")
        print(f"{'Destination':<12}{'Cost':<8}{'Next Hop'}")
        for dest, (cost, next_hop) in routing_table.items():
            print(f"{dest:<12}{cost:<8}{next_hop}")
        print()
