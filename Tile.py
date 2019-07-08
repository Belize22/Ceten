from abc import ABC


class Tile(ABC):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.edges = []
        super().__init__()
