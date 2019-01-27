import pygame
from Board import Board
from BoardFacade import BoardFacade

class Catan:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("First Window")
        self.screen = pygame.display.set_mode((680, 640))
        self.bf = BoardFacade(Board(), self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.update()
                if event.type == pygame.QUIT:
                    running = False

    def update(self):
        self.bf.draw()
        pygame.display.flip()

game = Catan()
game.run()
