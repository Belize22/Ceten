from Corner import Corner
from Button import Button
import math
import pygame
import pdb

class CornerFacade(Button):
	colour = {
		"WHITE" : (255, 255, 255),
		"YELLOW" : (255, 180, 0),
		"BLUE" : (0, 0, 255),
		"RED" : (255, 0, 0),
		"GREY" : (128, 128, 128),
		"BLACK" : (0, 0, 0)
	}

	player_to_colour_mapping = [colour.get("WHITE"), 
								colour.get("YELLOW"), 
								colour.get("BLUE"), 
								colour.get("RED")]

	def __init__(self, position, corner, screen):
		super().__init__(position,"",screen)
		self.center = position
		self.corner = corner
		self.screen = screen
		self.radius = 10
		self.rect   = None	
		self.draw()

	def in_boundaries(self, position):
		if math.sqrt((self.center[0]-position[0])**2+(self.center[1]-position[1])**2) < self.radius:
			return True
		else:
			return False

	def update(self, player):
		self.corner.update(player.id)
		self.draw()
	
	def draw(self):
		if (self.corner.ownership != 0):
			self.rect = pygame.draw.circle(self.screen, self.player_to_colour_mapping[self.corner.ownership-1], self.center, self.radius,0)
			if self.corner.settlement == "city":
				self.rect = pygame.draw.circle(self.screen, self.colour.get("BLACK"), self.center, round(self.radius/2), 3)
		self.rect = pygame.draw.circle(self.screen, self.colour.get("BLACK"), self.center, self.radius,3)

	def on_click(self):
		super().on_click()
		print("Clicked corner: " + corner.relational_id)