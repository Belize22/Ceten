import pygame
from TileFacade import TileFacade
from Tile import Tile
class Catan:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("First Window")
        self.screen = pygame.display.set_mode((640, 640))
	t = Tile("test", 2)
	self.tf = TileFacade(t, self.screen, [320,320], 20)
	

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
		self.update()
                if event.type == pygame.QUIT:
                    running = False

    def update(self):
	self.tf.draw()
	pygame.display.flip()

game = Catan()
game.run()
