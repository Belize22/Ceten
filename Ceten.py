from BoardFacade import BoardFacade
from PublicPlayerFacade import PublicPlayerFacade
from PrivatePlayerFacade import PrivatePlayerFacade
from CurrentPhase import CurrentPhase
from CurrentGamePhase import CurrentGamePhase
from CurrentTradePhase import CurrentTradePhase

import pygame


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
        self.board_facade.set_initial_feedback_message(
            self.private_player_facade)
        self.board_facade.update_phase_panel()
        self.board_facade.update_feedback_panel()

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
        mouse_pos = pygame.mouse.get_pos()
        phase, game_phase = self.board_facade.get_current_phases()
        if phase == CurrentPhase.SETUP_PHASE.value:
            self.board_facade.build_component(
                mouse_pos, self.private_player_facade)
        elif (self.board_facade.end_turn_button.in_boundaries(mouse_pos)
              and phase == CurrentPhase.VICTORY_PHASE.value):
            self.start_game()
        elif self.board_facade.roll_dice_button.in_boundaries(mouse_pos):
            self.board_facade.roll_dice()
        elif (self.board_facade.in_boundaries(mouse_pos)
                and game_phase == CurrentGamePhase.ROBBER.value):
            self.board_facade.place_robber(mouse_pos)
        elif self.board_facade.end_turn_button.in_boundaries(mouse_pos):
            self.board_facade.render_control_menu()
            self.board_facade.end_turn(self.private_player_facade)
        elif self.board_facade.maritime_trade_button.in_boundaries(mouse_pos):
            self.board_facade.begin_maritime_trade()
            self.private_player_facade.begin_maritime_trade()
        elif self.private_player_facade.resource_submit_button.in_boundaries(
                mouse_pos):
            self.private_player_facade.advance_maritime_trade()
            trade_phase = self.private_player_facade.current_trading_phase
            if trade_phase == CurrentTradePhase.NONE.value:
                self.board_facade.end_maritime_trade()
        elif game_phase == CurrentGamePhase.BUILDING.value:
            self.board_facade.build_component(
                mouse_pos, self.private_player_facade)

        self.board_facade.update_phase_panel()
        self.board_facade.update_feedback_panel()


game = Ceten()
game.run()
