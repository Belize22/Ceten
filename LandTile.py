from Tile import Tile


class LandTile(Tile):
    def __init__(self, coordinates, resource):
        super().__init__(coordinates)
        self.corners = []
        self.resource = resource
        self.activation_value = 0
        self.robber = False
