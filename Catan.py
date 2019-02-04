from Board import Board
from Player import Player
from BoardFacade import BoardFacade
from NextPhaseButton import NextPhaseButton
from RollButton import RollButton
from PlayerFacade import PlayerFacade
import pygame

class Catan:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pilgrims of Ceten (Catan Clone)")
        b = Board()
        b.connectEdges()
        self.screen = pygame.display.set_mode((680, 940))
        self.bf = BoardFacade(b, self.screen)
        self.screen.fill((0, 51, 204))
        self.roll_dice_button = RollButton((600,600), "Roll Dice", self.screen)
        self.next_phase_button = NextPhaseButton((100,700), "", self.screen)
        self.clock = pygame.time.Clock()
        self.player_facades = []
        self.player_facades.append(PlayerFacade(Player("Player1"), (340,740), self.screen))
        self.player_facades.append(PlayerFacade(Player("Player2"), (340,740), self.screen))
        self.player_facades.append(PlayerFacade(Player("Player3"), (340,740), self.screen))
        self.player_facades.append(PlayerFacade(Player("Player4"), (340,740), self.screen))
        self.active_robber = False
        self.has_rolled = False
        self.current = 0
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
        self.player_facades[self.current].draw()
        pygame.display.flip()
        self.clock.tick(15)

    def handle_mouse(self):
        print("Is the Robber Active? " + str(self.active_robber))
        mouse_pos = pygame.mouse.get_pos()
        if self.roll_dice_button.in_boundaries(mouse_pos) and self.active_robber == False and self.has_rolled == False:
            self.roll_dice_button.on_click()
            self.active_robber = self.roll_dice_button.on_roll()
            if self.active_robber == False:
                for pf in self.player_facades:
                	pf.gather( self.bf.get_resources(self.roll_dice_button.roll) ) 
                self.next_phase_button.on_roll_next()
            else:
                self.next_phase_button.on_roll_robber()
            self.has_rolled = True
        if self.bf.in_boundaries(mouse_pos) and self.active_robber == True:
            print("I got the tile!")
            rtf = self.bf.find_robber()
            print(str(type(rtf)))
            rtf.set_robber(False)
            tf = self.bf.find_tile_at(mouse_pos)
            tf.set_robber(True)
            self.active_robber = False
        if self.has_rolled == True and self.active_robber == False:
            self.current+=1
            self.current %= 4
            self.has_rolled = False
            self.next_phase_button.reset()

game = Catan()
game.run()
