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

    """run:
    This is the main game loop of Ceten. Detects when the user has
    clicked on the game window and will quit the game when the
    user desires.
    """
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

    """handle_mouse:
    This is the mouse control handler for the game loop. This is
    the basis of playing Ceten since no keyboard controls have
    been implemented yet and is therefore responsible for
    allowing the user to get involved with Ceten's game mechanics.
    """
    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        phase, game_phase = self.board_facade.get_current_phases()
        # Scenarios outside of Game phase
        if phase == CurrentPhase.SETUP_PHASE.value:
            self.board_facade.build_component(
                mouse_pos, self.private_player_facade)
        elif (self.board_facade.end_turn_button.in_boundaries(mouse_pos)
              and phase == CurrentPhase.VICTORY_PHASE.value):
            self.start_game()
        # Scenarios within game phase.
        elif self.board_facade.roll_dice_button.in_boundaries(mouse_pos):
            self.board_facade.roll_dice(self.private_player_facade)
        elif (self.board_facade.in_boundaries(mouse_pos)
                and game_phase == CurrentGamePhase.ROBBER.value):
            self.board_facade.place_robber(
                mouse_pos, self.private_player_facade)
        elif self.board_facade.end_turn_button.in_boundaries(mouse_pos):
            self.board_facade.render_control_menu()
            self.board_facade.end_turn(self.private_player_facade)
        elif self.board_facade.maritime_trade_button.in_boundaries(mouse_pos):
            self.board_facade.current_feedback = "Deposit resources!"
            self.board_facade.begin_maritime_trade()
            self.private_player_facade.begin_maritime_trade()
        # This section advances through the maritime trade phases and
        # displays the appropriate feedback message depending on the
        # trade phase.
        elif self.private_player_facade.resource_submit_button.in_boundaries(
                mouse_pos):
            self.private_player_facade.advance_maritime_trade()
            trade_phase = self.private_player_facade.current_trading_phase
            if trade_phase == CurrentTradePhase.NONE.value:
                self.board_facade.current_feedback = ""
                self.board_facade.end_maritime_trade(
                    self.private_player_facade)
            elif trade_phase == CurrentTradePhase.WITHDRAW.value:
                self.board_facade.current_feedback = (
                    "Withdraw "
                    + str(self.private_player_facade.
                          get_maritime_trade_points())
                    + " resources!")
        # Handles the use of increment and decrement buttons for resources
        # during maritime trading.
        elif game_phase == CurrentGamePhase.MARITIME_TRADE.value:
            self.private_player_facade.click_increment_for_maritime_trade(
                mouse_pos)
            self.private_player_facade.click_decrement_for_maritime_trade(
                mouse_pos)
        elif game_phase == CurrentGamePhase.BUILDING.value:
            self.board_facade.build_component(
                mouse_pos, self.private_player_facade)
        self.board_facade.update_phase_panel()
        self.board_facade.update_feedback_panel()


game = Ceten()
game.run()
