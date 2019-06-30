from Board import Board
from Player import Player
from BoardFacade import BoardFacade
from PublicPlayerFacade import PublicPlayerFacade
from PrivatePlayerFacade import PrivatePlayerFacade
import pygame
import random


class Ceten:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pilgrims of Ceten (Catan Clone)")
        self.screen = pygame.display.set_mode((900, 525))
        self.screen.fill((91, 146, 176))
        self.board_facade = None
        self.clock = pygame.time.Clock()
        self.num_players = None
        self.public_player_facades = None
        self.private_player_facade = None
        self.current_phase = 1
        self.start_game()

    def start_game(self):
        self.num_players = 4
        self.board_facade = BoardFacade(self.screen, self.num_players)
        self.board_facade.render_control_menu()
        players = self.board_facade.retrieve_players()
        self.public_player_facades = []
        for player in players:
            self.public_player_facades.append(
                PublicPlayerFacade(player, (340, 0), self.screen))
        for pf in self.public_player_facades:
            pf.initialize_panels()
        self.board_facade.board.change_current_player(players[0])
        self.private_player_facade = PrivatePlayerFacade(
            players[0], (340, 0), self.screen)
        self.board_facade.update_phase_panel()

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
        self.private_player_facade.draw()
        for pf in self.public_player_facades:
            pf.draw()
        pygame.display.flip()
        self.clock.tick(15)

    def handle_mouse(self):
        self.board_facade.feedback_panel.update("")
        mouse_pos = pygame.mouse.get_pos()
        if (self.board_facade.roll_dice_button.
                in_boundaries(mouse_pos)
                and self.current_phase == 1):
            self.current_phase = self.roll_dice()

        if (self.board_facade.in_boundaries(mouse_pos) and
                self.current_phase == 2):
            self.current_phase = self.board_facade.place_robber(mouse_pos)

        if (self.board_facade.end_turn_button.in_boundaries(mouse_pos)
                and self.current_phase == 3):
            self.current_phase = self.end_turn()

        if self.current_phase == 3:
            self.build_component(mouse_pos)

        self.board_facade.update_phase_panel()

    def setup_phase(self, mouse_pos):
        cf = self.board_facade.find_corner_at(mouse_pos)
        # Next player places settlement if current player successfully
        # places a settlement.
        if cf is not None:
            past_ownership = cf.corner.ownership
            self.board_facade.place_settlement(
                cf, self.private_player_facade)
            if self.reverse_turn_order:
                if (cf.corner.ownership ==
                        self.private_player_facade.player.id
                        and cf.corner.ownership != past_ownership):
                    self.board_facade.board.produce_initial_resources(
                        cf.corner,
                        self.private_player_facade.player)
                    self.current -= 1
            else:
                if (cf.corner.ownership ==
                        self.private_player_facade.player.id):
                    self.current += 1
            if self.current == 0:  # Denotes end of setup phase.
                self.current += 1
                self.setup_phase_active = False
                self.reverse_turn_order = False
                self.board_facade.phase_panel.update("Roll the Dice!")
            # Denotes the second turn of the setup phase.
            if self.current == len(self.public_player_facades) + 1:
                self.current -= 1
                self.reverse_turn_order = True
            if (self.reverse_turn_order and self.current != 0\
                    and cf.corner.ownership != past_ownership):
                self.board_facade.feedback_panel.update(
                    self.public_player_facades[self.current - 1].player.name
                    + ", place second settlement!")
            elif self.current != 1 and cf.corner.ownership != past_ownership:
                self.board_facade.feedback_panel.update(
                    self.public_player_facades[self.current - 1].player.name
                    + ", place first settlement!")

    def roll_dice(self):
        return self.board_facade.roll_dice()

    def build_component(self, mouse_pos):
        player = self.private_player_facade.get_player()
        self.board_facade.build_component(mouse_pos, player)

    def end_turn(self):
        self.board_facade.render_control_menu()
        return self.board_facade.end_turn(self.private_player_facade)


game = Ceten()
game.run()
