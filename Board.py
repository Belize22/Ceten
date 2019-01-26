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
	"12" : 2,
	}

	def __init__(self, tile_count = 19):
		self.tiles = []
		while len(Board.resources) > 0 and len(Board.activation_values) > 0:
			rs, rs_count  = random.choice(Board.resources.items())
			if (rs_count < 1):
				Board.resources.pop(rs)
				continue
			av, av_count = random.choice(Board.activation_values.items())
			if (av_count < 1):
				Board.activation_values.pop(av)
				continue
			self.tiles.append(Tile(rs,av))
			Board.resources[rs]-= 1
			Board.activation_values[av]-=1

	def randomize(self):
		seed = self.__random_tile()
		#generate a random ring of tiles around the seed tile	
		for e in seed.edges:
			if(e.connected_tiles != 2):
				t = self.__random_tile()
				e.adjacent_tiles.append(t)
				t.edges.append(e)
						
	def __random_tile(self):
		return self.tiles.get( random.randomint(0,len(self.tiles)) )
	
	def str(self):
		ret = ""
		for t in self.tiles:
			ret+=t.str()					
b = Board()
print b.str()
b.randomize()

