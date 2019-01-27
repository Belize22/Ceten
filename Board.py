from Tile import Tile
from Edge import Edge
from Corner import Corner
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
			print("TEST: " + rs)
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

	#def randomize(self):
	#	seed = self.__random_tile()
	#	#generate a random ring of tiles around the seed tile	
	#	for e in seed.edges:
	#		if(e.connected_tiles != 2):
	#			t = self.__random_tile()
	#			e.adjacent_tiles.append(t)
	#			t.edges.append(e)
						
	#def __random_tile(self):
	#	return self.tiles[random.randint(0,len(self.tiles))]

	def connectEdges(self):
		num_circles = 2;
		total_tile_quantity = get_product_sum(num_circles)
		val = 1
		level = 1

		while val < total_tile_quantity:
			level_tile_quantity = get_product_sum(level)
			nth_tile_being_iterated = 1
			if (level == 1):           #Middle Level
				while nth_tile_being_iterated < 6*level+1:
					second_corner = Corner()
					third_corner = Corner()

					if (nth_tile_being_iterated == 1):
						first_corner = Corner()
						final_corner = first_corner

					setEdges(self.tiles[val], self.tiles[val-1], first_corner, second_corner)

					if (nth_tile_being_iterated == 6*level):
						third_corner = final_corner
					if (nth_tile_being_iterated > 1):
						setEdges(self.tiles[val], self.tiles[0], first_corner, third_corner)
					if (nth_tile_being_iterated == 6*level):
						bridge_corner = Corner()
						setEdges(self.tiles[val], self.tiles[1], third_corner, bridge_corner)
						print("CORNERS: " + str(self.tiles[0].edgesConnectedToCorner(third_corner)))

					if (nth_tile_being_iterated == 1):
						first_corner = second_corner
					else:
						first_corner = third_corner

					nth_tile_being_iterated = nth_tile_being_iterated + 1
					val = val + 1
				level = level + 1
				val = 100
			else:                       #Outer Level
				adjacent_tile_of_previous_level = val - 6*(level-1)
				tiles_on_current_level_iterated = 0
				while nth_tile_being_iterated < 6*level+1:
					setEdges(self.tiles[val], self.tiles[val-1])
					setEdges(self.tiles[val], self.tiles[adjacent_tile_of_previous_level])

					if (val > 7 and nth_tile_being_iterated % 2 == 1):
						adjacent_tile_of_previous_level += 1
						setEdges(self.tiles[val], self.tiles[adjacent_tile_of_previous_level])

					if (nth_tile_being_iterated == 6*level):
						setEdges(self.tiles[val], self.tiles[val - 6*level+1])
					
					lone_edges_to_generate = 3 - (nth_tile_being_iterated % 2)

					for j in range(lone_edges_to_generate):
						setEdge(self.tiles[val])

					nth_tile_being_iterated = nth_tile_being_iterated + 1
					val = val + 1
	
		count = 1
		for t in self.tiles:
			corners_of_edges = []
			for e in t.edges:
				for c in e.corners:
					corners_of_edges.append(c)

			corners_of_current_tile = set(corners_of_edges)
			info = "Tile #" + str(count) + ": " + str(t.numEdges()) + " edges, " \
				 + str(len(corners_of_current_tile)) + " corners, Resource: " + t.resource
			print(info)
			count += 1


	def board_str(self):
		ret = ""
		count = 1;
		for t in self.tiles:
			print("TILE #" + str(count))
			ret += ("TILE #" + str(count) + t.str())
			count += 1


def setEdge(tile):
	edge = Edge()
	tile.addEdge(edge)
	
def setEdges(tile1, tile2, corner1, corner2):
	edge = Edge()
	edge.addCorner(corner1)
	edge.addCorner(corner2)
	tile1.addEdge(edge)
	tile2.addEdge(edge)

def get_product_sum(num):
	sum = 0
	num += 1
	for i in range(num):
		if (i > 0):
			sum += 6*i
		else:
			sum += 1
	return sum
