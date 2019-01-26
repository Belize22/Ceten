from Tile import Tile
import random

class Board:
	resources = {
	"ore"    : 3,
	"desert" : 1,
	"brick"  : 3,
	"wool"   : 4,
	"grain"  : 4,
	"lumber" : 4
	}
	activation_values = {
	"2"  : 1
	"3"  : 2
	"4"  : 2
	"5"  : 2
	"6"  : 2
	"8"  : 2 
	"9"  : 2
	"10" : 2
	"11" : 2
	"12" : 2
	}

	def __init__(self, tile_count = 19):
		self.tiles = []
		while len(resources) > 0 and len(activation_value) > 0:
			rs, rs_count  = random.choice(resources.items())
			if (rs_count < 1):
				resources.pop(rs)
				continue
			av, av_count = random.choice(activation_values.items())
			if (av_count < 1):
				activation_values.pop(av)
				continue
			self.append(Tile(rs,av))
			resources[rs]-= 1
			activation_values[av]-=1
		
