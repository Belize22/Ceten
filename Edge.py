from Corner import Corner
from Tile import Tile

class Edge:
	def __init__(self,corners = [],tiles = []):
		self.edge_corners = corners
		self.connected_tiles = tiles
