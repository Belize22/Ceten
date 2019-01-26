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
			rs, rs_count = random.choice(list(Board.resources.items()))
			print(rs)
			if (rs_count < 1):
				Board.resources.pop(rs)
				continue
			av, av_count = random.choice(list(Board.activation_values.items()))
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
		return self.tiles[random.randint(0,len(self.tiles))]

	def connectEdges(self):
		num_circles = 2;
		total_tile_quantity = get_exponential_sum(num_circles)
		val = 1
		level = 1

		while val < total_tile_quantity:
			level_tile_quantity = get_exponential_sum(level)
			i = level_tile_quantity - 6**level
			print("NUM: " + str(i))
			#print("LTQ: " + str(level_tile_quantity))
			print("6**level: " + str(6**level))
			if (level == 1):           #2nd to inner-most circle
				while i < 6**level+1:
					print("ON TILE #" + str(i))
					printNums(val, val-1)
					if (i > 0):
						printNums(val, 0)
					if (i == 6**level):
						printNums(val, 1)
					i = i + 1
					val = val + 1
				level = level + 1
			else:
				val = 100

	def str(self):
		ret = ""
		for t in self.tiles:
			ret += t.str()

def printNums(num1, num2):
		print ("(" + str(num1) + ", " + str(num2) + ")")

def get_exponential_sum(num):
		sum = 0
		num += 1
		for i in range(num):
			sum += 6**i
		return sum
