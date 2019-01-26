from Edge import Edge
from Tile import Tile

class Corner:
	def __init__(self, edges = [], tiles = [], settlement = "none", ownership = "none"):
		self.edges = edges
		self.connected_tiles = tiles
        self.settlement = settlement
        self.ownership = ownership

    def str(self):
        return "Corner Settlement: " + self.settlement + ", Owned By:" + self.ownership \  
               + ", Edge Count: " + repr(len(self.edges)) +  ", Tile Count: " \
               + repr(len(self.adjacent_tiles)))  