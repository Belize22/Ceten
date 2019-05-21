from enum import Enum


class GamePieceType(Enum):
    ROAD = 0
    SETTLEMENT = 1
    CITY = 2


class GamePieceBank:
    ROAD_QUANTITY = 15
    SETTLEMENT_QUANTITY = 5
    CITY_QUANTITY = 4

    def __init__(self):
        self.game_pieces = []
        for i in range(3):
            if i == GamePieceType.ROAD.value:
                self.game_pieces.append(self.ROAD_QUANTITY)
            elif i == GamePieceType.SETTLEMENT.value:
                self.game_pieces.append(self.SETTLEMENT_QUANTITY)
            elif i == GamePieceType.CITY.value:
                self.game_pieces.append(self.CITY_QUANTITY)

    def place_road(self):
        self.game_pieces[GamePieceType.ROAD.value] -= 1

    def place_settlement(self):
        self.game_pieces[GamePieceType.SETTLEMENT.value] -= 1

    # Upgrading to a city effectively gives the player back a settlement.
    def place_city(self):
        self.game_pieces[GamePieceType.CITY.value] -= 1
        self.game_pieces[GamePieceType.SETTLEMENT.value] += 1
