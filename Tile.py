class Tile:

	def __init__(self, resource, activation_value, corners = [], edges = [], adjacent_tiles = []):
		self.resource 	      = resource
		self.activation_value = activation_value
		self.corners 	      = corners
		self.edges	      = edges
		self.adjacent_tiles   = adjacent_tiles	
	def str(self):
		return "Tile: " + self.resource + ", Value: " + repr(self.activation_value) \
			   + ", Edge Count: "+ repr(len(self.edges)) + ", Corner Count: " \
			   + repr(len(self.corners) + ", Tile Count: " + repr(len(self.adjacent_tiles))) 

