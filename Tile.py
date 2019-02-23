from Edge import Edge

class Tile:

	def __init__(self, resource, activation_value):
		self.relational_id    = ""
		self.resource 	      = resource
		self.activation_value = activation_value
		self.edges	          = []
		self.adjacent_tiles   = []
		self.robber           = False	
	def addEdge(self, edge):
		self.edges.append(edge)

	def numEdges(self):
		return len(self.edges)
	
	def numEdgesConnectedToCorner(self, corner):
		count = 0
		for e in self.edges:
			if (e.hasCorner(corner) == "true"):
				count += 1
		return count
				
	def str(self):
		print("Tile: " + self.resource)
		return "Tile: " + self.resource + ", Value: " + repr(self.activation_value) + ", Edge Count: "+ repr(len(self.edges)) + ", Tile Count: " + repr(len(self.adjacent_tiles)) + ", Edge Count: " + repr(len(self.edges)) 
