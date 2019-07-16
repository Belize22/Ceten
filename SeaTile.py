from Tile import Tile


class SeaTile(Tile):
    def __init__(self, coordinates, tile_aggregate, port="None"):
        super().__init__(coordinates, tile_aggregate)
        self.port = port
