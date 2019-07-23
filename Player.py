from ResourceBank import ResourceBank
from GamePieceBank import GamePieceBank
from GamePieceType import GamePieceType
from PortType import PortType


class Player:
    VICTORY_POINTS_TO_WIN = 6

    def __init__(self, id, name, board):
        self.id = id
        self.turn_priority = id
        self.name = name
        self.board = board
        self.resource_bank = ResourceBank()
        self.game_piece_bank = GamePieceBank()
        self.trade_rates = [4, 4, 4, 4, 4]  # Always start off at 4:1 rate.
        self.resources_at_start_of_trade_phase = [0, 0, 0, 0, 0]
        self.maritime_trade_points = 0

    '''
    has_player_won:
    This determines whether the player has the sufficient victory
    points to win Ceten. As of now, victory points are calculated:
    as follows: victory_points = placed_settlements + placed_cities*2
    '''
    def has_player_won(self):
        victory_points = 0
        victory_points += (
                self.game_piece_bank.STARTING_QUANTITIES[
                    GamePieceType.SETTLEMENT.value]
                - self.game_piece_bank.game_pieces[
                    GamePieceType.SETTLEMENT.value])
        victory_points += (
                self.game_piece_bank.STARTING_QUANTITIES[
                    GamePieceType.CITY.value]
                - self.game_piece_bank.game_pieces[GamePieceType.CITY.value])*2
        return victory_points >= self.VICTORY_POINTS_TO_WIN

    def update_players_trade_rates(self, ports):
        for p in ports:
            if p == PortType.STANDARD.value:  # Turn all 4:1 to 3:1's
                for i in range(0, len(self.trade_rates)):
                    if self.trade_rates[i] > 3:
                        self.trade_rates[i] = 3
            else:  # Turn resource trade rate that port specifies into 2:1
                self.trade_rates[p - 1] = 2

    def set_resources_before_starting_trade_phase(self):
        self.resources_at_start_of_trade_phase = \
            self.resource_bank.resources.copy()

    def retrieve_player_name(self):
        return str(self.name)



