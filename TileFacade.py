from Tile import Tile
import pygame
import math
class TileFacade:
	colour = {
		"RED" : (255, 0, 0),
		"GREEN" : (0, 51, 0),
		"GREY" : (102, 102, 102),
		"LIGHT_GREEN" : (77, 255, 77),
		"YELLOW" : (255, 255, 0),
		"WHITE" : (255, 255, 255),
	}
	texture = {
		"ore" : "./res/oreHex.gif",
		"desert": "./res/desertHex.gif",
		"brick": "./res/clayHex.gif",
		"wool": "./res/sheepHex.gif",
		"grain": "./res/wheatHex.gif",
		"lumber":"./res/woodHex.gif",
	}
	
	def __init__(self, tile, screen, centre = [0, 0], scale = 1):
		self.tile   	   = tile
		self.screen 	   = screen
		self.points 	   = self.__hex_pointlist_generator(scale - 3, centre)
		self.border_points = self.__hex_pointlist_generator(scale, centre)
		self.colour 	   = self.__set_colour(self.tile.resource)
		self.texture = self.__set_texture(self.tile.resource)
		self.text	   = ""
		self.centre	   = [round(centre[0]), round(centre[1])]
		self.rect	   = None

	def draw(self):
		pygame.draw.polygon(self.screen, (0, 0, 0), self.border_points, 0)
		self.rect = pygame.draw.polygon(self.screen, self.colour, self.points, 0)
		self.texture = pygame.transform.scale(self.texture, self.rect.size)
		self.screen.blit(self.texture, self.rect)
		self.text  = self.__set_activation_value( str(self.tile.activation_value)) 
		
		if str(self.tile.activation_value) != "0" or self.tile.robber == True:
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
		if self.tile.robber == True:
			activation_value = "R"
		return font.render(activation_value, 1, (10,10,10))
			
	def __set_colour(self,resource):
		if resource == "lumber":
			return TileFacade.colour["GREEN"]
		elif resource == "brick":
			return TileFacade.colour["RED"] 
		elif resource == "ore":
			return TileFacade.colour["GREY"]
		elif resource == "wool":
			return TileFacade.colour["LIGHT_GREEN"]
		elif resource == "grain":
			return TileFacade.colour["YELLOW"]
		else:
			#desert
			return TileFacade.colour["WHITE"]

	def __set_texture(self,resource):
		if resource == "lumber":
			return pygame.image.load(TileFacade.texture["lumber"])
		elif resource == "brick":
			return pygame.image.load(TileFacade.texture["brick"])
		elif resource == "ore":
			return pygame.image.load(TileFacade.texture["ore"])
		elif resource == "wool":
			return pygame.image.load(TileFacade.texture["wool"])
		elif resource == "grain":
			return pygame.image.load(TileFacade.texture["grain"])
		else:
			#desert
			return pygame.image.load(TileFacade.texture["desert"])
	def set_robber(self,flag):
		self.tile.robber = flag

	def str(self):
		return "TileFacade with Points: " + str(self.points) + "\n" + self.tile.str()
