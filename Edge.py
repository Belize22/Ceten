from EdgeCardinality import EdgeCardinality
from CornerCardinality import CornerCardinality

class Edge:
    def __init__(self, ownership=0):
        self.tiles = []
        self.ownership = ownership
        self.port = None

    def update(self, ownership):
        self.ownership = ownership

    def road_is_not_occupied(self):
        does_edge_have_ownership = False
        if self.ownership == 0:
            does_edge_have_ownership = True
        return does_edge_have_ownership

    def road_can_be_placed(self, player):
        does_adjacent_edge_belong_to_player = False
        corners_of_edge = []
        neighboring_edges = []
        tile_next_to_edge = self.tiles[0] # Only need one tile to get corners.
        for i in range(0, len(EdgeCardinality)):
            if tile_next_to_edge.edges[i] == self:
                next_index = (i + 1) % len(EdgeCardinality)
                if (tile_next_to_edge.corners[i].ownership == 0
                        or tile_next_to_edge.corners[i].ownership == player):
                    corners_of_edge.append(tile_next_to_edge.corners[i])
                if (tile_next_to_edge.corners[next_index].ownership == 0
                        or tile_next_to_edge.corners[
                            next_index].ownership == player):
                    corners_of_edge.append(
                        tile_next_to_edge.corners[next_index])
        for c in corners_of_edge:
            for t in c.tiles:
                for i in range(0, len(CornerCardinality)):
                    if t.corners[i] == c:
                        previous_index = (i - 1) % len(EdgeCardinality)
                        next_index = (i + 1) % len(EdgeCardinality)
                        if t.edges[previous_index] in neighboring_edges:
                            neighboring_edges.append(t.edges[previous_index])
                        if t.edges[next_index] in neighboring_edges:
                            neighboring_edges.append(t.edges[next_index])
        for ne in neighboring_edges:
            if ne.ownership == player:
                does_adjacent_edge_belong_to_player = True
        return does_adjacent_edge_belong_to_player


