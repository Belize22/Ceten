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
        self.active_robber = False;
    
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
        print("Is the Robber Active? " + str(self.active_robber))
        mouse_pos = pygame.mouse.get_pos()
        if self.button.in_boundaries(mouse_pos) and self.active_robber == False:
            self.button.on_click()
            self.active_robber = self.button.on_roll()
            if self.active_robber == False:
                self.pf.gather( self.bf.get_resources(self.button.roll) ) 
        if self.bf.in_boundaries(mouse_pos) and self.active_robber == True:
            print("I got the tile!")
            rtf = self.bf.find_robber()
            print(str(type(rtf)))
            rtf.set_robber(False)
            tf = self.bf.find_tile_at(mouse_pos)
            tf.set_robber(True)
            self.active_robber = False
            

game = Catan()
game.run()
