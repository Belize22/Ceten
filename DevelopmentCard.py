from enum import Enum

class DevelopmentCardType(Enum):
    KNIGHT = 1
    VICTORY_POINT = 2
    YEAR_OF_PLENTY = 3
    MONOPOLY = 4
    ROAD_BUILDING = 5


class DevelopmentCard:
    cost_sheep = 1
    cost_grain = 1
    cost_ore = 1

    def __init__(self, type):
        self.type = type
