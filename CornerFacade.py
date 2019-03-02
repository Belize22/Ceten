from Corner import Corner
import pygame

class CornerFacade:
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
		self.center = position
		self.corner = corner
		self.screen = screen
		self.radius = 10
		self.rect   = None	
		self.draw()

	def in_boundaries(self, pos):
		return self.rect.collidepoint(pos)
	
	def draw(self):
		if (self.corner.ownership != 0):
			self.rect = pygame.draw.circle(self.screen, self.player_to_colour_mapping[self.corner.ownership-1], self.center, self.radius,0)
			self.rect = pygame.draw.circle(self.screen, self.colour.get("BLACK"), self.center, self.radius,3)
			if self.corner.settlement == "city":
				self.rect = pygame.draw.circle(self.screen, self.colour.get("BLACK"), self.center, round(self.radius/2), 3)