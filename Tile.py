from Edge import Edge

class Tile:

	def __init__(self, resource, activation_value):
		self.resource 	      = resource
		self.activation_value = activation_value
		self.edges	          = []
		self.adjacent_tiles   = []
		
	def addEdge(self, edge):
		self.edges.append(edge)

	def numEdges(self):
		return len(self.edges)

	def str(self):
		print("Tile: " + self.resource)
		return "Tile: " + self.resource + ", Value: " + repr(self.activation_value) \
			   + ", Edge Count: "+ repr(len(self.edges)) + ", Tile Count: " \
			   + repr(len(self.adjacent_tiles)) 
