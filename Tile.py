from Edge import Edge

class Tile:
    def __init__(self, resource, activation_value):
        self.physical_id = ""
        self.relational_id = ""
        self.edges = []
        self.resource = resource
        self.activation_value = activation_value
        self.robber = False	
        
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def num_edges_connected_to_corner(self, corner):
        count = 0
        for e in self.edges:
            if (e.has_corner(corner)):
                count += 1
        return count
                
    def str(self):
        return "Tile: Resource - " + self.resource \
               + ", ID - " + self.relational_id
