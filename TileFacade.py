from Tile import Tile
import pygame
import math
class TileFacade:
	def __init__(self, tile, screen, centre = [0, 0], scale = 1):
		self.tile = tile
		self.screen = screen
		self.points = self.__hex_pointlist_generator(scale, centre)
	
	def draw(self):
		pygame.draw.polygon(self.screen, (255,   0,   0), self.points, 0)	
	
	def __hex_pointlist_generator(self, scale, centre):
		ret = []
		for i in range(6):
			deg = 60.0 * i - 30.0
			rad = math.pi / 180.0 * deg
			ret.append([centre[0] + scale * math.cos(rad), centre[1] + scale * math.sin(rad)])
		return ret	
		
		

