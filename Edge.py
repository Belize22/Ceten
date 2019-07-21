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

    def road_can_be_placed(self, ownership):
        does_adjacent_edge_belong_to_player = False
        corners_of_edge = self.get_corners_of_edge(ownership)
        neighboring_edges = []  # Only need one tile to get corners.
        for c in corners_of_edge:
            neighboring_edges += self.get_neighboring_edges(c)
        for ne in neighboring_edges:
            if ne.ownership == ownership:
                does_adjacent_edge_belong_to_player = True
        return does_adjacent_edge_belong_to_player

    def road_can_be_placed_during_setup(self, ownership):
        road_next_to_current_settlement = False
        corners_of_edge = self.get_corners_of_edge(ownership)
        neighboring_edges = []
        for c in corners_of_edge:
            if c.ownership == ownership:
                neighboring_edges += self.get_neighboring_edges(c)
        if len(neighboring_edges) > 0:
            road_next_to_current_settlement = True
        for ne in neighboring_edges:
            if ne.ownership == ownership:
                road_next_to_current_settlement = False
        return road_next_to_current_settlement

    def get_corners_of_edge(self, ownership):
        corners_of_edge = []
        tile_next_to_edge = self.tiles[0]
        for i in range(0, len(EdgeCardinality)):
            if tile_next_to_edge.edges[i] == self:
                next_index = (i + 1) % len(EdgeCardinality)
                if (tile_next_to_edge.corners[i].ownership == 0
                        or tile_next_to_edge.corners[
                            i].ownership == ownership):
                    corners_of_edge.append(tile_next_to_edge.corners[i])
                if (tile_next_to_edge.corners[next_index].ownership == 0
                        or tile_next_to_edge.corners[
                            next_index].ownership == ownership):
                    corners_of_edge.append(
                        tile_next_to_edge.corners[next_index])
        return corners_of_edge

    def get_neighboring_edges(self, corner):
        neighboring_edges = []
        for t in corner.tiles:
            for i in range(0, len(CornerCardinality)):
                if t.corners[i] == corner:
                    previous_index = (i - 1) % len(EdgeCardinality)
                    if t.edges[previous_index] not in neighboring_edges:
                        neighboring_edges.append(t.edges[previous_index])
                    if t.edges[i] not in neighboring_edges:
                        neighboring_edges.append(t.edges[i])
        return neighboring_edges


