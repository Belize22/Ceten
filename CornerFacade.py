from Corner import Corner
import pygame

class CornerFacade:

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
		self.rect = pygame.draw.circle(self.screen, (255, 0, 0), self.center, self.radius,0)

	
