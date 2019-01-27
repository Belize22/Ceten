class Player:
    def __init__(self, name_):

        # resources
        self.name = name_
        self.num_lumber = 0
        self.num_wool = 0
        self.num_grain = 0
        self.num_Brick = 0
        self.num_ore = 0

        # pieces
        self.num_settlements = 5
        self.num_cities = 4
        self.num_roads = 15

        # development cards
        self.dev_cards = []
