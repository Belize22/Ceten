from Corner import Corner
from Tile import Tile

class Edge:
	def __init__(self, corners = [], tiles = [], ownership="none", port="none"):
		self.corners = corners
		self.connected_tiles = tiles
		self.ownership = ownership
		self.port = port

    def str(self):
        return "Edge Ownership: " + self.settlement + ", Port: " + repr(self.port) \
		       + ", Edge Count: "+ repr(len(self.edges)) + ", Tile Count: " \ 
			   + repr(len(self.adjacent_tiles))) 