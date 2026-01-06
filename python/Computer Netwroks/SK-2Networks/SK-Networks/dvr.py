class Router:
    def __init__(self, name):  
        self.name = name
        self.routing_table = {}  
        self.neighbors = {}  

    def add_neighbor(self, neighbor_name, cost):
        """Add a neighbor router and cost to reach it."""
        self.neighbors[neighbor_name] = cost
        
        self.routing_table[neighbor_name] = cost

    def update_routing_table(self, routers):
        """Update the routing table based on neighbors' information."""
        updated = False
        for neighbor_name, cost in self.neighbors.items():
            
            neighbor_router = next((router for router in routers if router.name == neighbor_name), None)
            
            if neighbor_router:
                
                for destination, neighbor_cost in neighbor_router.routing_table.items():
                    new_cost = cost + neighbor_cost
                    
                    if destination not in self.routing_table or self.routing_table[destination] > new_cost:
                        self.routing_table[destination] = new_cost
                        updated = True
        return updated

    def __str__(self):  
        """String representation of the routing table."""
        table_str = f"Routing Table for Router {self.name}:\n"
        for destination, cost in self.routing_table.items():
            table_str += f"Destination: {destination}, Cost: {cost}\n"
        return table_str


def distance_vector_routing(routers, iterations=10):
    """Run the Distance Vector Routing Algorithm."""
    for i in range(iterations):
        print(f"\nIteration {i + 1}:")
        updated = False
        
        for router in routers:
            if router.update_routing_table(routers):
                updated = True
        if not updated:
            print("No updates in this iteration, the algorithm has converged.")
            break

        
        for router in routers:
            print(router)



router_A = Router('A')
router_B = Router('B')
router_C = Router('C')
router_D = Router('D')
router_E = Router('E')


router_A.add_neighbor('B', 1)
router_A.add_neighbor('C', 3)
router_B.add_neighbor('A', 1)
router_B.add_neighbor('C', 1)
router_B.add_neighbor('D', 2)
router_C.add_neighbor('A', 3)
router_C.add_neighbor('B', 1)
router_C.add_neighbor('D', 1)
router_D.add_neighbor('B', 2)
router_D.add_neighbor('C', 1)
router_D.add_neighbor('E', 3)
router_E.add_neighbor('D', 3)


routers = [router_A, router_B, router_C, router_D, router_E]


distance_vector_routing(routers, iterations=10)
