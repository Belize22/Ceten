from Tile import Tile
from ResourceType import ResourceType
from EdgeCardinality import EdgeCardinality


class LandTile(Tile):
    def __init__(self, coordinates, resource):
        super().__init__(coordinates)
        self.corners = []
        self.resource = resource
        self.activation_value = None
        if self.resource == ResourceType.DESERT.value:
            self.robber = True
        else:
            self.robber = False

    def get_adjacent_land_tiles(self, land_tiles):
        base_coordinate = self.coordinates
        adjacent_land_tiles = []
        for direction in EdgeCardinality:
            adjacent_coordinate = self.change_coordinate(
                base_coordinate, direction.value)
            for t in land_tiles:
                if t.coordinates == adjacent_coordinate:
                    adjacent_land_tiles.append(t)
        return adjacent_land_tiles



