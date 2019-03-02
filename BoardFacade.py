from Board import Board
from Tile import Tile
from TileFacade import TileFacade
import pygame
import math
import random

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
		tiles = self.board.getTilesOrderedByPhysicalID()
		for q, r in BoardFacade.grid_coordinates:
			s = - q - r
			tf =TileFacade(tiles.pop(0), 
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

	def produceResources(self, roll):
 		return self.board.produceResources(roll)

	#will always return at least one robber
	def find_robber(self):
		t = self.board.find_robber()
		print("Robber Found! " + t.str())
		for tf in self.tile_facades:
			if tf.tile == t:
				print("Robber Facade Found! " + str(tf))
				return tf

	def find_tile_at(self, pos):
		for tf in self.tile_facades:
			if tf.rect.collidepoint(pos):
				return tf

	def in_boundaries(self,pos):
		if self.find_tile_at(pos) != None:
			return True
		return False	

	def draw(self):
		for tf in self.tile_facades:
			tf.draw()
