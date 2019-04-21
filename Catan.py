from Board import Board
from Player import Player
from BoardFacade import BoardFacade
from Button import Button
from RollButton import RollButton
from PlayerFacade import PlayerFacade
import pygame


class Catan:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pilgrims of Ceten (Catan Clone)")
        board = Board()
        board.connect_board()
        self.screen = pygame.display.set_mode((900, 525))
        self.board_facade = BoardFacade(board, self.screen)
        self.screen.fill((91, 146, 176))
        pygame.draw.rect(self.screen, (178, 155, 130),
                         ((self.screen.get_width()*0.8, self.screen.get_height()*0.5),
                          (self.screen.get_width()*0.2,
                           self.screen.get_height()*0.5)),
                         0)
        self.roll_dice_button = RollButton((int(self.screen.get_width()*0.9), 275), "Roll Dice",
                                           self.screen)
        self.end_turn_button = Button((int(self.screen.get_width()*0.9), 425), "End Turn",
                                      self.screen)
        self.clock = pygame.time.Clock()
        self.num_players = 4
        self.player_facades = []
        for i in range(1, self.num_players+1):
            self.player_facades.append(PlayerFacade(Player(i, "Player" + str(i)), 
                                       (340, 0), self.screen))
        for pf in self.player_facades:
            self.board_facade.board.players.append(pf.player)
        self.board_facade.phase_panel.update("Roll the Dice!")
        board.simulate_starting_phase()
        self.active_robber = False
        self.active_building = False
        self.has_rolled = False
        self.current = 1

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
        self.board_facade.draw()
        self.player_facades[self.current-1].draw()
        for pf in self.player_facades:
            pf.draw_public()
        pygame.display.flip()
        self.clock.tick(15)

    def handle_mouse(self):
        self.board_facade.feedback_panel.update("")
        print("Is the Robber Active? " + str(self.active_robber))
        mouse_pos = pygame.mouse.get_pos()
        
        if self.active_building:
            cf = self.board_facade.find_corner_at(mouse_pos)
            if cf is not None:
                self.board_facade.place_settlement(cf,
                                                   self.player_facades[
                                                    self.current-1])
                print("Clicked Corner: " + cf.corner.relational_id,
                      "Settlement: " + cf.corner.settlement,
                      "Ownership: " + str(cf.corner.ownership))

        if (self.roll_dice_button.in_boundaries(mouse_pos) and
                not self.active_robber and not self.has_rolled):
            self.roll_dice_button.on_click()
            self.active_robber = self.roll_dice_button.on_roll()
            if not self.active_robber:
                self.board_facade.produce_resources(self.roll_dice_button.roll)
                for pf in self.player_facades:
                    print(pf.player.str())            
                self.board_facade.phase_panel.update("Build something from your Inventory")
            else:
                self.board_facade.phase_panel.update("Move the robber and rob a nearby settlement")
            self.has_rolled = True

        if self.board_facade.in_boundaries(mouse_pos) and self.active_robber:
            tf = self.board_facade.find_tile_at(mouse_pos)
            if int(tf.tile.relational_id) < 19:
                print("I got the tile!")
                rtf = self.board_facade.find_robber()
                print(str(type(rtf)))
                rtf.set_robber(False)
                tf.set_robber(True)
                self.active_robber = False  
                self.board_facade.phase_panel.update("Build something from your Inventory")

        if self.has_rolled and not self.active_robber:
            self.active_building = True

        if self.end_turn_button.in_boundaries(mouse_pos) and self.active_building:
            self.current += 1
            if self.current > self.num_players:
                self.current = 1
            self.has_rolled = False
            self.active_building = False
            self.board_facade.phase_panel.update("Roll the Dice!")


game = Catan()
game.run()
