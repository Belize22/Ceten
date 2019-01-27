from Tile import Tile
import pygame
import math
class TileFacade:
	RED = (255, 0, 0)
	GREEN = (0, 51, 0)
	GREY = (102, 102, 102)
	LIGHT_GREEN = (77, 255, 77)
	YELLOW = (255, 255, 0)
	WHITE = (255, 255, 255)
	def __init__(self, tile, screen, centre = [0, 0], scale = 1):
		self.tile   	   = tile
		self.screen 	   = screen
		self.points 	   = self.__hex_pointlist_generator(scale - 3, centre)
		self.border_points = self.__hex_pointlist_generator(scale, centre)
		self.colour 	   = self.__set_colour(self.tile.resource)
		if str(self.tile.activation_value) != "0" :
			self.text 	   = self.__set_activation_value( str(self.tile.activation_value)) 
		self.centre	   = [round(centre[0]), round(centre[1])]
	def draw(self):
		pygame.draw.polygon(self.screen, (0, 0, 0), self.border_points, 0)
		pygame.draw.polygon(self.screen, self.colour, self.points, 0)
		if str(self.tile.activation_value) != "0":
			pygame.draw.circle(self.screen, (228, 205, 180), self.centre, 20, 0)
			self.screen.blit(self.text,[self.centre[0] - 11, self.centre[1] - 8] )
	
	def __hex_pointlist_generator(self, scale, centre):
		ret = []
		for i in range(6):
			deg = 60.0 * i - 30.0
			rad = math.pi / 180.0 * deg
			ret.append([centre[0] + scale * math.cos(rad), centre[1] + scale * math.sin(rad)])
		return ret
	def __set_activation_value(self, activation_value):
		font = pygame.font.Font(None, 36)
		return font.render(activation_value, 1, (10,10,10))
			
	def __set_colour(self,resource):
		if resource == "lumber":
			return TileFacade.GREEN
		elif resource == "brick":
			return TileFacade.RED 
		elif resource == "ore":
			return TileFacade.GREY
		elif resource == "wool":
			return TileFacade.LIGHT_GREEN
		elif resource == "grain":
			return TileFacade.YELLOW
		else:
			#desert
			return TileFacade.WHITE
	def str(self):
		return "TileFacade with Points: " + str(self.points) + "\n" + self.tile.str()
