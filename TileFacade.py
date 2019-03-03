from Tile import Tile
import pygame
import math
import pdb

class TileFacade:
	colour = {
		"RED" : (255, 0, 0),
		"GREEN" : (0, 51, 0),
		"GREY" : (102, 102, 102),
		"LIGHT_GREEN" : (77, 255, 77),
		"YELLOW" : (255, 255, 0),
		"WHITE" : (255, 255, 255),
		"LIGHT_BLUE": (91, 146, 176)
	}
	texture = {
		"ore" : "./res/oreHex.gif",
		"desert": "./res/desertHex.gif",
		"brick": "./res/clayHex.gif",
		"wool": "./res/sheepHex.gif",
		"grain": "./res/wheatHex.gif",
		"lumber":"./res/woodHex.gif",
		"standard_port_0":"./res/miscPort0.gif",
		"standard_port_1":"./res/miscPort1.gif",
		"standard_port_2":"./res/miscPort2.gif",
		"standard_port_3":"./res/miscPort3.gif",
		"standard_port_4":"./res/miscPort4.gif",
		"standard_port_5":"./res/miscPort5.gif",
		"specialized_port_0":"./res/port0.gif",
		"specialized_port_1":"./res/port1.gif",
		"specialized_port_2":"./res/port2.gif",
		"specialized_port_3":"./res/port3.gif",
		"specialized_port_4":"./res/port4.gif",
		"specialized_port_5":"./res/port5.gif",
		"water": "./res/waterHex.gif"
	}
	
	def __init__(self, tile, screen, centre = [0, 0], scale = 1, port_direction = -1):
		self.tile   	    = tile
		self.screen 	    = screen
		self.points 	    = self.__hex_pointlist_generator(scale - 3, centre)
		self.border_points  = self.__hex_pointlist_generator(scale, centre)
		self.colour 	    = self.__set_colour(self.tile.resource)
		self.port_direction = port_direction
		self.texture        = self.__set_texture(self.tile.resource)
		self.text	        = ""
		self.centre	        = [round(centre[0]), round(centre[1])]
		self.rect	        = None

	def draw(self):
		pygame.draw.polygon(self.screen, (0, 0, 0), self.border_points, 0)
		self.rect = pygame.draw.polygon(self.screen, self.colour, self.points, 0)
		self.texture = pygame.transform.scale(self.texture, self.rect.size)
		self.screen.blit(self.texture, self.rect)
		self.text  = self.__set_activation_value( str(self.tile.activation_value)) 
		
		if str(self.tile.activation_value) != "0" or self.tile.robber == True:
			color = (228, 205, 180)
			if (self.tile.robber == True):
				color = (27, 50, 75)			
			pygame.draw.circle(self.screen, color, self.centre, 20, 0)
			self.screen.blit(self.text,[self.centre[0] - 11, self.centre[1] - 8])

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
		if "lumber" in resource:
			return TileFacade.colour["GREEN"]
		elif "brick" in resource:
			return TileFacade.colour["RED"] 
		elif "ore" in resource:
			return TileFacade.colour["GREY"]
		elif "wool" in resource:
			return TileFacade.colour["LIGHT_GREEN"]
		elif "grain" in resource:
			return TileFacade.colour["YELLOW"]
		elif resource == "desert":
			return TileFacade.colour["WHITE"]
		else:
			return TileFacade.colour["LIGHT_BLUE"]

	def __set_texture(self,resource):
		if "lumber" in resource:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["specialized_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["lumber"])
		elif "brick" in resource:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["specialized_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["brick"])
		elif "ore" in resource:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["specialized_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["ore"])
		elif "wool" in resource:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["specialized_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["wool"])
		elif "grain" in resource:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["specialized_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["grain"])
		elif resource == "desert":
			return pygame.image.load(TileFacade.texture["desert"])
		else:
			if "port" in resource:
				return pygame.image.load(TileFacade.texture["standard_port_" + str(self.port_direction)])
			else:
				return pygame.image.load(TileFacade.texture["water"])

	def set_robber(self,flag):
		self.tile.robber = flag

	#def grabPortDirection(self, tile):
	#	if tile_id % 2 == 0 and tile_id/2 %:


	def str(self):
		return "TileFacade with Points: " + str(self.points) + "\n" + self.tile.str()
