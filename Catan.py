import pygame
from Board import Board
from Player import Player
from BoardFacade import BoardFacade
from RollButton import RollButton
from PlayerFacade import PlayerFacade
class Catan:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pilgrims of Ceten")
        self.screen = pygame.display.set_mode((680, 940))
        self.bf = BoardFacade(Board(), self.screen)
        self.screen.fill((0, 51, 204))
        self.button = RollButton((600,600), "Roll the Dice!", self.screen)
        self.clock = pygame.time.Clock()
        self.pf = PlayerFacade(Player("Gertrude"), (340,740), self.screen)
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP: 
                    self.handle_mouse()
                if event.type == pygame.QUIT:
                    running = False
                self.update()
    def update(self):
        self.bf.draw()
        self.pf.draw()
        pygame.display.flip()
        self.clock.tick(15)

    def handle_mouse(self):
        if self.button.in_boundaries(pygame.mouse.get_pos()):
            self.button.on_click()
game = Catan()
game.run()
