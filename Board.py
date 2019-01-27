from Tile import Tile
import random

class Board:
	resources = {
	"ore"    : 3,
	"desert" : 1,
	"brick"  : 3,
	"wool"   : 4,
	"grain"  : 4,
	"lumber" : 4,
	}
	activation_values = {
	"2"  : 1,
	"3"  : 2,
	"4"  : 2,
	"5"  : 2,
	"6"  : 2,
	"8"  : 2,
	"9"  : 2,
	"10" : 2,
	"11" : 2,
	"12" : 1,
	}

	def __init__(self, tile_count = 19):
		self.tiles = []
		while len(Board.resources) > 0 and len(Board.activation_values) > 0:
			(rs, rs_count)  = random.choice(list(Board.resources.items()))
			if (rs_count < 1):
				Board.resources.pop(rs)
				continue
			if (rs == "desert"):
				t = Tile(rs,0)
				t.robber = True
				self.tiles.append(t)
				Board.resources[rs]-= 1
				continue
			(av, av_count) = random.choice(list(Board.activation_values.items()))
			if (av_count < 1):
				Board.activation_values.pop(av)
				continue
			self.tiles.append(Tile(rs,av))
			Board.resources[rs]-= 1
			Board.activation_values[av]-=1

	def connect_tiles(self):
		seed = self.__random_tile()
		#generate a random ring of tiles around the seed tile	
		for e in seed.edges:
			if(e.connected_tiles != 2):
				t = self.__random_tile()
				e.adjacent_tiles.append(t)
				t.edges.append(e)
				inner_ring.append(t)
						
	def __random_tile(self):
		return self.tiles[ random.randint(0,len(self.tiles) - 1) ]
	def tile_list_copy(self):
		ret = []
		for t in self.tiles:
			ret.append(t)
		return ret		
	def str(self):
		ret = "Board has the Following Tiles:\n"
		for t in self.tiles:
			ret+=t.str() + "\n"
		return ret



