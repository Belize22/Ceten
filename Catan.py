from Board import Board
from Player import Player
from BoardFacade import BoardFacade
from Button import Button
from RollButton import RollButton
from PlayerFacade import PlayerFacade
import pygame
import random


class Catan:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pilgrims of Ceten (Catan Clone)")
        self.board = None
        self.screen = pygame.display.set_mode((900, 525))
        self.board_facade = None
        self.screen.fill((91, 146, 176))
        self.clock = pygame.time.Clock()
        self.roll_dice_button = None
        self.end_turn_button = None
        self.num_players = None
        self.player_facades = None
        self.active_robber = None
        self.active_building = None
        self.has_rolled = None
        self.current = None
        self.winner_present = None
        self.start_new_game = None
        self.setup_phase = None
        self.reverse_turn_order = None
        self.start_game()

    def start_game(self):
        self.board = Board()
        self.board_facade = BoardFacade(self.board, self.screen)
        pygame.draw.rect(
            self.screen, (178, 155, 130),
            ((self.screen.get_width()*0.8, self.screen.get_height()*0.5),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.roll_dice_button = RollButton(
            (int(self.screen.get_width()*0.9), 275), "Roll Dice", self.screen)
        self.end_turn_button = Button(
            (int(self.screen.get_width()*0.9), 425), "End Turn", self.screen)
        self.num_players = 4
        self.player_facades = []
        for i in range(1, self.num_players+1):
            self.player_facades.append(
                PlayerFacade(
                    Player(i, "Player" + str(i)), (340, 0), self.screen))
        self.player_facades = self.randomize_turn_order(self.player_facades)
        for pf in self.player_facades:
            self.board_facade.board.players.append(pf.player)
        self.board_facade.phase_panel.update("Roll the Dice!")
        #self.board.simulate_starting_phase()
        self.active_robber = False
        self.active_building = False
        self.has_rolled = False
        self.current = 1
        self.winner_present = False
        self.start_new_game = False
        self.setup_phase = True
        self.reverse_turn_order = False
        # Give each player free resources to place initial settlements.
        for i in range(0, len(self.player_facades)):
            self.player_facades[i].player.resource_bank. \
                collect_resources([2, 2, 2, 2, 0])
            self.player_facades[i].player.resource_bank.validate_transaction()

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

        if self.setup_phase:
            cf = self.board_facade.find_corner_at(mouse_pos)
            # Next player places settlement if current player successfully
            # places a settlement.
            if cf is not None:
                self.board_facade.place_settlement(
                    cf, self.player_facades[self.current - 1])
                if self.reverse_turn_order:
                    if (cf.corner.ownership ==
                            self.player_facades[self.current-1].player.id):
                        self.current -= 1
                else:
                    if (cf.corner.ownership ==
                            self.player_facades[self.current-1].player.id):
                        self.current += 1
                if self.current == 0:  # Denotes end of setup phase.
                    self.setup_phase = False
                    self.reverse_turn_order = False
                # Denotes the second turn of the setup phase.
                if self.current == len(self.player_facades) + 1:
                    self.current -= 1
                    self.reverse_turn_order = True
        else:
            if self.active_building:
                cf = self.board_facade.find_corner_at(mouse_pos)
                if cf is not None:
                    self.board_facade.place_settlement(
                        cf, self.player_facades[self.current-1])
                    if (self.player_facades[self.current-1].player
                            .retrieve_victory_points() >= 10):
                        self.winner_present = True
                    print(
                        "Clicked Corner: " + cf.corner.relational_id,
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
                    self.board_facade.phase_panel.update(
                        "Build something from your Inventory")
                else:
                    self.board_facade.phase_panel.update(
                        "Move the robber and rob a nearby settlement")
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
                    self.board_facade.phase_panel.update(
                        "Build something from your Inventory")

            if self.has_rolled and not self.active_robber:
                self.active_building = True

            if (self.end_turn_button.in_boundaries(mouse_pos)
                    and self.active_building):
                pygame.draw.rect(
                    self.screen, (178, 155, 130),
                    ((self.screen.get_width() * 0.8,
                      self.screen.get_height() * 0.5),
                     (self.screen.get_width() * 0.2,
                      self.screen.get_height() * 0.5)), 0)
                self.roll_dice_button.update("Roll Dice!")
                self.end_turn_button.update("End Turn")
                if self.start_new_game:
                    self.start_game()
                elif self.winner_present:
                    pygame.draw.rect(
                        self.screen, (178, 155, 130),
                        ((self.screen.get_width() * 0.8,
                          self.screen.get_height() * 0.5),
                         (self.screen.get_width() * 0.2,
                          self.screen.get_height() * 0.5)), 0)
                    self.board_facade.phase_panel.update("Game Over!")
                    self.board_facade.feedback_panel.update(
                        self.player_facades[self.current-1].player.name
                        + " has won Catan!")
                    self.end_turn_button.update("New Game")
                    self.start_new_game = True
                else:
                    self.current += 1
                    if self.current > self.num_players:
                        self.current = 1
                    self.has_rolled = False
                    self.active_building = False
                    self.board_facade.phase_panel.update("Roll the Dice!")

    def randomize_turn_order(self, player_facades):
        for i in range(0, len(player_facades)-1):
            random_index = random.randint(0, len(player_facades)-1)
            player_facades[i].player.turn_priority, \
                player_facades[random_index].player.turn_priority = \
                player_facades[random_index].player.turn_priority, \
                player_facades[i].player.turn_priority
            player_facades[i], player_facades[random_index] = \
                player_facades[random_index], player_facades[i]
        return player_facades


game = Catan()
game.run()
