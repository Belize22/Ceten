from Board import Board
from Player import Player
from BoardFacade import BoardFacade
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
        self.num_players = None
        self.player_facades = None
        self.active_building = None
        self.has_rolled = None
        self.current = None
        self.winner_present = None
        self.start_new_game = None
        self.setup_phase_active = None
        self.reverse_turn_order = None
        self.start_game()

    def start_game(self):
        self.board = Board()
        self.board_facade = BoardFacade(self.board, self.screen)
        self.board_facade.render_control_menu()
        self.num_players = 4
        self.player_facades = []
        for i in range(1, self.num_players+1):
            self.player_facades.append(
                PlayerFacade(
                    Player(i, "Player" + str(i)), (340, 0), self.screen))
        self.player_facades = self.randomize_turn_order(self.player_facades)
        for pf in self.player_facades:
            pf.initialize_public_panels()
        self.has_rolled = False
        self.current = 1
        self.winner_present = False
        self.start_new_game = False
        self.setup_phase_active = True
        self.reverse_turn_order = False
        # Give each player free resources to place initial settlements.
        for i in range(0, len(self.player_facades)):
            self.player_facades[i].player.resource_bank. \
                collect_resources([2, 2, 2, 2, 0])
            self.player_facades[i].player.resource_bank.validate_transaction()
        self.board_facade.phase_panel.update("Setup Phase!")
        self.board_facade.feedback_panel.update(
            self.player_facades[0].player.name + ", place first settlement!")

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
        print("Is the Robber Active? " + str(self.board_facade.board.active_robber))
        mouse_pos = pygame.mouse.get_pos()

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
                self.place_robber(mouse_pos)

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
                cf, self.player_facades[self.current - 1])
            if self.reverse_turn_order:
                if (cf.corner.ownership ==
                        self.player_facades[self.current - 1].player.id
                        and cf.corner.ownership != past_ownership):
                    self.board.produce_initial_resources(
                        cf.corner,
                        self.player_facades[self.current - 1].player)
                    self.current -= 1
            else:
                if (cf.corner.ownership ==
                        self.player_facades[self.current - 1].player.id):
                    self.current += 1
            if self.current == 0:  # Denotes end of setup phase.
                self.current += 1
                self.setup_phase_active = False
                self.reverse_turn_order = False
                self.board_facade.phase_panel.update("Roll the Dice!")
            # Denotes the second turn of the setup phase.
            if self.current == len(self.player_facades) + 1:
                self.current -= 1
                self.reverse_turn_order = True
            if (self.reverse_turn_order and self.current != 0\
                    and cf.corner.ownership != past_ownership):
                self.board_facade.feedback_panel.update(
                    self.player_facades[self.current - 1].player.name
                    + ", place second settlement!")
            elif self.current != 1 and cf.corner.ownership != past_ownership:
                self.board_facade.feedback_panel.update(
                    self.player_facades[self.current - 1].player.name
                    + ", place first settlement!")

    def roll_dice(self):
        roll = self.board_facade.roll_dice()
        if not self.board_facade.board.active_robber:
            player_list = []
            for i in range(0, len(self.player_facades)):
                player_list.append(self.player_facades[i].player)
            self.board_facade.produce_resources(roll, player_list)
            for pf in self.player_facades:
                print(pf.player.str())
            self.board_facade.phase_panel.update(
                "Build something from your Inventory")
        else:
            self.board_facade.phase_panel.update(
                "Move the robber and rob a nearby settlement")
        self.has_rolled = True

    def place_robber(self, mouse_pos):
        tf = self.board_facade.find_tile_at(mouse_pos)
        if int(tf.tile.relational_id) < 19:
            print("I got the tile!")
            rtf = self.board_facade.find_robber()
            print(str(type(rtf)))
            rtf.set_robber(False)
            tf.set_robber(True)
            self.board_facade.board.active_robber = False
            self.board_facade.phase_panel.update(
                "Build something from your Inventory")

    def build_component(self, mouse_pos):
        cf = self.board_facade.find_corner_at(mouse_pos)
        if cf is not None:
            self.board_facade.place_settlement(
                cf, self.player_facades[self.current - 1])
            if (self.player_facades[self.current - 1].player
                    .retrieve_victory_points() >= 10):
                self.winner_present = True
            print(
                "Clicked Corner: " + cf.corner.relational_id,
                "Settlement: " + cf.corner.settlement,
                "Ownership: " + str(cf.corner.ownership))

    def end_turn(self):
        self.board_facade.render_control_menu()
        if self.start_new_game:
            self.start_game()
        elif self.winner_present:
            self.board_facade.render_control_menu()
            self.board_facade.phase_panel.update("Game Over!")
            self.board_facade.feedback_panel.update(
                self.player_facades[self.current - 1].player.name
                + " has won Catan!")
            self.board_facade.end_turn_button.update("New Game")
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
