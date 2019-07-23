from EdgeCardinality import EdgeCardinality
from CornerCardinality import CornerCardinality
from SettlementLevel import SettlementLevel


class Corner:
    def __init__(self, settlement=SettlementLevel.NONE.value, ownership=0):
        self.tiles = []
        self.settlement = settlement
        self.ownership = ownership

    def update(self, player):
        if self.settlement == SettlementLevel.NONE.value:
            self.ownership = player.id
        if self.settlement < len(SettlementLevel):
            self.settlement += 1
        self.update_players_trade_rates(player)

    def is_settlement_not_settled_by_current_player(self, ownership):
        does_corner_have_ownership = False
        if ownership == self.ownership or self.ownership == 0:
            does_corner_have_ownership = True
        return does_corner_have_ownership

    def are_neighboring_corners_settled(self):
        is_an_adjacent_corner_settled = False
        neighboring_corners = []
        for t in self.tiles:
            for i in range(0, len(t.corners)):
                if t.corners[i] == self:
                    next_index = (i + 1) % len(CornerCardinality)
                    if t.corners[i] not in neighboring_corners:
                        neighboring_corners.append(t.corners[i])
                    if t.corners[next_index] not in neighboring_corners:
                        neighboring_corners.append(t.corners[next_index])
        for nc in neighboring_corners:
            if nc != self and nc.ownership != 0:
                is_an_adjacent_corner_settled = True
                break
        return is_an_adjacent_corner_settled

    def corner_adjacent_to_players_road(self, ownership):
        is_settlement_adjacent_to_corresponding_road = False
        neighboring_edges = self.get_neighboring_edges(self.tiles)
        for nc in neighboring_edges:
            if nc.ownership == ownership:
                is_settlement_adjacent_to_corresponding_road = True
        return is_settlement_adjacent_to_corresponding_road

    def update_players_trade_rates(self, player):
        ports = self.ports_of_edges_on_corner()
        player.update_players_trade_rates(ports)

    def ports_of_edges_on_corner(self):
        neighboring_edges = self.get_neighboring_edges(self.tiles)
        ports = []
        for nc in neighboring_edges:
            if nc.port is not None:
                ports.append(nc.port)
        return ports

    def get_neighboring_edges(self, tiles):
        neighboring_edges = []
        for t in tiles:
            for i in range(0, len(EdgeCardinality)):
                if t.corners[i] == self:
                    previous_index = (i - 1) % len(CornerCardinality)
                    if t.edges[previous_index] not in neighboring_edges:
                        neighboring_edges.append(t.edges[previous_index])
                    if t.edges[i] not in neighboring_edges:
                        neighboring_edges.append(t.edges[i])
        return neighboring_edges



