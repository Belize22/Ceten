class GamePieceBank:
    def __init__(self):
        self.roads = 15
        self.settlements = 5
        self.cities = 4

    def place_road(self):
        self.roads -= 1

    def place_settlement(self):
        self.settlements -= 1

    def place_city(self):
        self.cities -= 1
        self.settlements += 1
