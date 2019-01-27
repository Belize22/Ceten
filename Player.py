class Player:
    def __init__(self, name):

        # resources
        self.name = name
        self.num_lumber = 0
        self.num_wool = 0
        self.num_grain = 0
        self.num_brick = 0
        self.num_ore = 0

        # pieces
        self.num_settlements = 5
        self.num_cities = 4
        self.num_roads = 15

        # development cards
        self.dev_cards = []

    def str(self):
        ret = "Player: " + str(self.name)
        ret += "\nPlayer Resources:\n" + "Wool: " + str(self.num_wool) + "\nLumber: " + str(self.num_lumber) + "\nGrain: " + str(self.num_grain) + "\nBrick: " + str(self.num_brick) + "\nOre: " + str(self.num_ore)
        ret += "\nPlayer Pieces:\n" + "Settlements: " + str(self.num_settlements) + "\nCities: " + str(self.num_cities) + "\nRoads: " + str(self.num_roads)
        return ret
