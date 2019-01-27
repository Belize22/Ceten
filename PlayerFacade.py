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
