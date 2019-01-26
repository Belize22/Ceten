from enum import Enum


class Development_card_type(Enum):
    Knight = 1
    Victory_Point = 2
    Year_Of_Plenty = 3
    Monopoly = 4
    Road_Building = 5


class Development_Card:

    cost_sheep = 1
    cost_grain = 1
    cost_ore = 1

    def __init__(self, _type):
        self.type = _type
