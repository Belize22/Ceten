from Board import Board
from Tile import Tile
from TileFacade import TileFacade
import pygame
import math

class BoardFacade:
	grid_coordinates = [
	(0,-2),
	(-1,-1),
	(-2,0),
	(1,-2),
	(0,-1),
	(-1,0),
	(-2,1),
	(2,-2),
	(1,-1),
	(0,0),
	(-1,1),
	(-2,2),
	(2,-1),
	(1,0),
	(0,1),
	(-1,2),
	(2,0),
	(1,1),
	(0,2),
	]

	def __init__(self, board, screen):
		self.board  = board
		self.screen = screen
		self.tile_facades = []
		self.__generate_facades()

	def __generate_facades(self, start = [320.0, 320.0], size = 70.0):
		tile_count = 0
		offset_y   = 0
		offset_x   = 0
		for q, r in BoardFacade.grid_coordinates:
			s = - q - r
			tf =TileFacade(self.board.tiles[tile_count], 
			  		  self.screen, 
					  [start[0] + s * size * math.sqrt(3.0) + offset_x, start[1] + 1.5 * q * size + offset_y], 
					   size)
			print (tf.str())
			self.tile_facades.append(tf)
			tile_count += 1
			#be careful tinkering with this code, it is tempermental
			if   tile_count == 3:
				offset_x = size * 0.87
			elif tile_count == 7:
				offset_x = size * 1.72
			elif tile_count == 12:
				offset_x = size * 1.72
			elif tile_count == 16:
				offset_x = size * 1.72
			else:
				offset_x -= size * math.sqrt(3.0)/2.0

	def draw(self):
		for tf in self.tile_facades:
			tf.draw()
