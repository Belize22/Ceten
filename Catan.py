import pygame
from TileFacade import TileFacade
from Tile import Tile
from Board import Board
class Catan:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("First Window")
		self.screen = pygame.display.set_mode((640, 640))
		t = Tile("test", 2)
		self.tf = TileFacade(t, self.screen, [320,320], 20)
	

	def run(self):
		running = True
		b = Board()
		print(b.board_str())
		b.connectEdges()

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
