from enum import Enum


class GamePieceType(Enum):
    ROAD = 0
    SETTLEMENT = 1
    CITY = 2


class GamePieceBank:
    STARTING_QUANTITIES = [15, 5, 4]

    def __init__(self):
        self.game_pieces = self.STARTING_QUANTITIES.copy()

    def place_road(self):
        self.game_pieces[GamePieceType.ROAD.value] -= 1

    def place_settlement(self):
        self.game_pieces[GamePieceType.SETTLEMENT.value] -= 1

    # Upgrading to a city effectively gives the player back a settlement.
    def place_city(self):
        self.game_pieces[GamePieceType.CITY.value] -= 1
        self.game_pieces[GamePieceType.SETTLEMENT.value] += 1
