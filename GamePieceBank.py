from enum import Enum


class GamePieceType(Enum):
    ROAD = 0
    SETTLEMENT = 1
    CITY = 2


class GamePieceBank:
    def __init__(self):
        self.game_pieces = []
        for i in range(3):
            if i == GamePieceType.ROAD.value:
                self.game_pieces.append(15)
            elif i == GamePieceType.SETTLEMENT.value:
                self.game_pieces.append(5)
            elif i == GamePieceType.CITY.value:
                self.game_pieces.append(4)

    def place_road(self):
        self.game_pieces[GamePieceType.ROAD.value] -= 1

    def place_settlement(self):
        self.game_pieces[GamePieceType.SETTLEMENT.value] -= 1

    def place_city(self):
        self.game_pieces[GamePieceType.CITY.value] -= 1
        self.game_pieces[GamePieceType.SETTLEMENT.value] += 1
