from ResourceBank import ResourceBank
from GamePieceBank import GamePieceBank
from GamePieceType import GamePieceType


class Player:
    VICTORY_POINTS_TO_WIN = 10

    def __init__(self, id, name):
        self.id = id
        self.turn_priority = id
        self.name = name
        self.resource_bank = ResourceBank()
        self.game_piece_bank = GamePieceBank()

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

    def retrieve_player_name(self):
        return str(self.name)



