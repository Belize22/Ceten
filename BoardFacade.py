from Board import Board
from Tile import Tile
from TileFacade import TileFacade
from CornerFacade import CornerFacade
import pygame
import math
import random
import pdb

class BoardFacade:
	grid_coordinates = [
	(0,-3),
	(-1,-2),
	(-2,-1),
	(-3,0),
	(1,-3),	
	#
	(0,-2),
	(-1,-1),
	(-2,0),
	#
	(-3,1),
	(2,-3),
	#
	(1,-2),
	(0,-1),
	(-1,0),
	(-2,1),
	#
	(-3,2),
	(3,-3),
	#
	(2,-2),
	(1,-1),
	(0,0),
	(-1,1),
	(-2,2),
	#
	(-3,3),
	(3,-2),
	#
	(2,-1),
	(1,0),
	(0,1),
	(-1,2),
	#
	(-2,3),
	(3,-1),
	#
	(2,0),
	(1,1),
	(0,2),
	#
	(-1,3),
	(3,0),
	(2,1),
	(1,2),
	(0,3)
	]

	def __init__(self, board, screen):
		self.board  = board
		self.screen = screen
		self.tile_facades = []
		self.corner_facades = []
		self.__generate_facades()
		
	def __generate_facades(self, start = [340.0, 340.0], size = 50.0):
		tile_count = 0
		offset_y   = 0
		offset_x   = 0
		tiles = self.board.getTilesOrderedByPhysicalID()
		for q, r in BoardFacade.grid_coordinates:
			s = - q - r
			current_tile = tiles.pop(0)
			tile_facade =TileFacade(current_tile, 
			  		  self.screen, 
					  [start[0] + s * size * math.sqrt(3.0) + offset_x, start[1] + 1.5 * q * size + offset_y], 
					   size)
			print (tile_facade.str())
			index = 0
			for tf in self.tile_facades:
				if int(tf.tile.relational_id) < int(tile_facade.tile.relational_id):
					index += 1
				else:
					break

			self.tile_facades.insert(index, tile_facade)
			tile_count += 1
			#be careful tinkering with this code, it is tempermental
			if tile_count == 4:
				offset_x = size * 0.87
			elif tile_count == 9:
				offset_x = size * 1.72
			elif tile_count == 15:
				offset_x = size * 2.6
			elif tile_count == 22:
				offset_x = size * 2.6
			elif tile_count == 28:
				offset_x = size * 2.6
			elif tile_count == 33:
				offset_x = size * 2.6
			else:
				offset_x -= size * math.sqrt(3.0)/2.0

		corners_of_tile = []
		for tf in self.tile_facades:
			for e in tf.tile.edges:
				for c in e.corners:
					if c not in corners_of_tile:
						corners_of_tile.append(c)
			for c in corners_of_tile:
				tiles_of_corner = []
				for e in c.edges:
					for t in e.tiles:
						if t not in tiles_of_corner:
							tiles_of_corner.append(t)
				tile_facade_reference_points = []
				for t in tiles_of_corner:
					for tf in self.tile_facades:
						if tf.tile == t:
							tile_facade_reference_points.append(tf)
				#pdb.set_trace()
				center_x = 0
				center_y = 0
				for tf in tile_facade_reference_points:
					center_x += tf.centre[0]/3
					center_y += tf.centre[1]/3
				corner_facade = CornerFacade([round(center_x), round(center_y)], c, self.screen)			
				insert_facade = True
				for cf in self.corner_facades:
					if (cf.center == corner_facade.center):
						insert_facade = False
						break
				if insert_facade == True:
					self.corner_facades.append(corner_facade)


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
		for cf in self.corner_facades:
			cf.draw()
