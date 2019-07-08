from Tile import Tile


class SeaTile(Tile):
    def __init__(self, coordinates, port="None"):
        super().__init__(coordinates)
        self.port = port
