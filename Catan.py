import pygame

class Catan:
	
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("First Window")
		pygame.display.set_mode((640,640))

	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False	


game = Catan()
game.run()
