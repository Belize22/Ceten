from Player import Player
import pygame

class PlayerFacade:

	def __init__(self, player, center, screen):
		self.player = player
		self.center = center
		self.screen = screen
	
	def draw(self):
		pygame.draw.rect(self.screen,
				(228, 205, 180), 
				((0, self.center[1]),(self.screen.get_width(), self.screen.get_height() - self.center[1])), 
				0)
	def gather(self, res_dict):
		self.player.num_wool 	+= res_dict["wool"]	
		self.player.num_grain 	+= res_dict["grain"]	
		self.player.num_brick 	+= res_dict["brick"]	
		self.player.num_ore 	+= res_dict["ore"]	
		self.player.num_lumber  += res_dict["lumber"]
		print(self.player.str())		
