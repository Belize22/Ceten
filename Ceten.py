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
        self.roll_dice_button = None
        self.num_players = None
        self.public_player_facades = None
        self.private_player_facade = None
        self.active_building = None
        self.has_rolled = None
        self.winner_present = None
        self.start_new_game = None
        self.setup_phase_active = None
        self.reverse_turn_order = None
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
        self.has_rolled = False
        self.winner_present = False
        self.start_new_game = False
        self.setup_phase_active = False
        self.reverse_turn_order = False
        # Give each player free resources to place initial settlements.
        #for i in range(0, len(self.public_player_facades)):
            #self.public_player_facades[i].player.resource_bank. \
            #    collect_resources([2, 2, 2, 2, 0])
            #self.public_player_facades[i].player.resource_bank.\
            #    validate_transaction()
        self.board_facade.phase_panel.update("Setup Phase!")
        self.board_facade.feedback_panel.update(
            self.public_player_facades[0].player.name
            + ", place first settlement!")

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

        '''
        button_num = self.public_player_facades[self.current - 1].\
            private_resource_incrementers.toggle_button_in_boundary(mouse_pos)
        if button_num != -1:
            print(self.public_player_facades[self.current - 1].player.name
                  + " clicked increment button #" + str(button_num))
        button_num = self.public_player_facades[self.current - 1]. \
            private_resource_decrementers.toggle_button_in_boundary(
            mouse_pos)
        if button_num != -1:
            print(self.public_player_facades[self.current - 1].player.name
                  + " clicked decrement button #" + str(button_num))

        if (self.public_player_facades[self.current - 1].resource_submit_button.
                in_boundaries(mouse_pos)):
            print(self.public_player_facades[self.current - 1].player.name
                  + " submitted resource content!")
        '''

        if self.setup_phase_active:
            self.setup_phase(mouse_pos)
        else:
            if self.active_building:
                self.build_component(mouse_pos)

            if (self.board_facade.roll_dice_button.
                    in_boundaries(mouse_pos)
                    and not self.board_facade.board.active_robber
                    and not self.has_rolled):
                self.roll_dice()

            if (self.board_facade.in_boundaries(mouse_pos) and
                    self.board_facade.board.active_robber):
                self.board_facade.place_robber(mouse_pos)

            if self.has_rolled and not self.board_facade.board.active_robber:
                self.active_building = True

            if (self.board_facade.end_turn_button.in_boundaries(mouse_pos)
                    and self.active_building):
                self.end_turn()

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
        self.board_facade.roll_dice()
        self.has_rolled = True

    def build_component(self, mouse_pos):
        player = self.private_player_facade.get_player()
        self.board_facade.build_component(mouse_pos, player)
        if (self.private_player_facade.player
                .retrieve_victory_points() >= 10):
            self.winner_present = True

    def end_turn(self):
        self.board_facade.render_control_menu()
        if self.start_new_game:
            self.start_game()
        elif self.winner_present:
            self.board_facade.render_control_menu()
            self.board_facade.phase_panel.update("Game Over!")
            self.board_facade.feedback_panel.update(
                self.public_player_facades[self.current - 1].player.name
                + " has won Catan!")
            self.board_facade.end_turn_button.update("New Game")
            self.start_new_game = True
        else:
            self.board_facade.end_turn(self.private_player_facade)
            self.has_rolled = False
            self.active_building = False


game = Ceten()
game.run()
