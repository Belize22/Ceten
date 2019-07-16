from abc import ABC
from Edge import Edge
from EdgeCardinality import EdgeCardinality


class Tile(ABC):
    def __init__(self, coordinate, tile_aggregate):
        self.coordinate = coordinate
        self.edges = []
        for direction in EdgeCardinality:
            self.edges.append(None)
        self.generate_edges(tile_aggregate)
        super().__init__()

    def generate_edges(self, tile_aggregate):
        base_coordinate = self.coordinate
        for direction in EdgeCardinality:
            adjacent_coordinate = self.change_coordinate(
                base_coordinate, direction.value)
            # Copy existing edges from adjacent tile of current direction
            for t in tile_aggregate:
                if t.coordinate == adjacent_coordinate:
                    contrary_edge_direction = (direction.value + 3) \
                                              % len(EdgeCardinality)
                    self.edges[direction.value] = t.edges[
                        contrary_edge_direction]
            # Generate new edge if adjacent tile for current direction doesn't
            # exist.
            if self.edges[direction.value] is None:
                self.edges[direction.value] = Edge()
            self.edges[direction.value].tiles.append(self)

    def get_adjacent_tiles(self, tiles):
        base_coordinate = self.coordinate
        adjacent_land_tiles = []
        for direction in EdgeCardinality:
            adjacent_coordinate = self.change_coordinate(
                base_coordinate, direction.value)
            for t in tiles:
                if t.coordinate == adjacent_coordinate:
                    adjacent_land_tiles.append(t)
        return adjacent_land_tiles

    '''
    change_coordinate:
    Allows the current coordinate of the map builder to be changed based
    on the specified direction.
    '''
    @staticmethod
    def change_coordinate(current_coordinate, direction):
        new_coordinate = current_coordinate.copy()
        # Horizontal Directions. Solely modifies x-coordinate
        if direction == EdgeCardinality.LEFT.value:
            new_coordinate[0] -= 1
        elif direction == EdgeCardinality.RIGHT.value:
            new_coordinate[0] += 1
        # Diagonal Directions. Always modifies y-coordinate, may
        # modify x-coordinate based on direction and parity of the sum
        # of the parity of the x-coordinate and the parity of the
        # sum of the x-coordinate and y-coordinate.
        elif direction == EdgeCardinality.TOP_LEFT.value:
            new_coordinate[0] -= (
                    1 - ((current_coordinate[0] + (
                          current_coordinate[0] + current_coordinate[1])) % 2))
            new_coordinate[1] -= 1
        elif direction == EdgeCardinality.TOP_RIGHT.value:
            new_coordinate[0] += (
                    (current_coordinate[0] + (
                     current_coordinate[0] + current_coordinate[1])) % 2)
            new_coordinate[1] -= 1
        elif direction == EdgeCardinality.BOTTOM_LEFT.value:
            new_coordinate[0] -= (
                    1 - ((current_coordinate[0] + (
                          current_coordinate[0] + current_coordinate[1])) % 2))
            new_coordinate[1] += 1
        else:  # Bottom-Right
            new_coordinate[0] += (
                    (current_coordinate[0] + (
                     current_coordinate[0] + current_coordinate[1])) % 2)
            new_coordinate[1] += 1
        return new_coordinate
