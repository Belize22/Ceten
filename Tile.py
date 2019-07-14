from abc import ABC
from EdgeCardinality import EdgeCardinality


class Tile(ABC):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.edges = []
        super().__init__()

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
