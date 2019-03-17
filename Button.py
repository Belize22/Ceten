import pygame

class Button:
	def __init__(self, position, dialog, screen):
		self.screen = screen
		(self.text_surf, 
		 self.text_box) = self.text_objects(dialog, 
		                                    pygame.font.Font(None, 36))
		self.text_box.center = position
		self.center = position
		screen.blit(self.text_surf, self.text_box)
	
	def text_objects(self, text, font):
    		text_surface = font.render(text, 1, (10, 10, 10))
    		return text_surface, text_surface.get_rect()

	def on_click(self):
		print ("Ping!")
		
	def in_boundaries(self, position):
		return self.text_box.collidepoint(position)	
