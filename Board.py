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
	def get_resources(self, roll):
		res_dict = {
			"wool"  : 0,
			"lumber": 0,
			"ore"   : 0,
			"brick" : 0,
			"grain" : 0
		}
		#todo check if the tile has an associated city or sentiment!
		for t in self.tiles:
			if str(t.activation_value) == str(roll) and t.robber == False:
					if t.resource == "wool":
						res_dict["wool"]+=1
					elif t.resource == "lumber":
						res_dict["lumber"]+=1
					elif t.resource == "ore":
        					res_dict["ore"]+=1
					elif t.resource == "brick":
        					res_dict["brick"]+=1
					elif t.resource == "grain":
        					res_dict["grain"]+=1
		return res_dict
	def __random_tile(self):
		return self.tiles[ random.randint(0,len(self.tiles) - 1) ]
	def tile_list_copy(self):
		ret = []
		for t in self.tiles:
			ret.append(t)
		return ret
	def find_robber(self):
		for t in self.tiles:
			if t.robber == True:
				return t
	def str(self):
		ret = "Board has the Following Tiles:\n"
		for t in self.tiles:
			ret+=t.str() + "\n"
		return ret



