from Tile import Tile
from Corner import Corner
from ResourceType import ResourceType
from EdgeCardinality import EdgeCardinality
from CornerCardinality import CornerCardinality


class LandTile(Tile):
    def __init__(self, coordinate, tile_aggregate, resource):
        super().__init__(coordinate, tile_aggregate)
        self.corners = []
        self.resource = resource
        self.activation_value = None
        for direction in CornerCardinality:
            self.corners.append(None)
        self.generate_corners(tile_aggregate)
        if self.resource == ResourceType.DESERT.value:
            self.robber = True
        else:
            self.robber = False

    def generate_corners(self, tile_aggregate):
        base_coordinate = self.coordinate
        for direction in EdgeCardinality:
            next_direction = (direction.value + 1) % len(EdgeCardinality)
            adjacent_coordinate = self.change_coordinate(
                base_coordinate, direction.value)
            # Copy existing corners from adjacent tile of current direction
            for t in tile_aggregate:
                if t.coordinate == adjacent_coordinate:
                    contrary_first_corner_direction = (direction.value - 2) \
                                                      % len(EdgeCardinality)
                    contrary_second_corner_direction = (direction.value + 3) \
                                                      % len(EdgeCardinality)
                    self.corners[direction.value] = t.corners[
                        contrary_first_corner_direction]
                    self.corners[next_direction] = t.corners[
                        contrary_second_corner_direction]
            # Generate new corners if adjacent tile for current direction
            # doesn't exist.
            if self.corners[direction.value] is None:
                self.corners[direction.value] = Corner()
            if self.corners[next_direction] is None:
                self.corners[next_direction] = Corner()
            self.corners[direction.value].tiles.append(self)
            self.corners[next_direction].tiles.append(self)



