from CornerCardinality import CornerCardinality
from SettlementLevel import SettlementLevel


class Corner:
    def __init__(self, settlement=SettlementLevel.NONE.value, ownership=0):
        self.tiles = []
        self.settlement = settlement
        self.ownership = ownership

    def update(self, ownership):
        if self.settlement == SettlementLevel.NONE.value:
            self.ownership = ownership
        if self.settlement < len(SettlementLevel):
            self.settlement += 1

    def does_corner_belong_to_a_player(self, ownership):
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
                    previous_index = (i - 1) % len(CornerCardinality)
                    next_index = (i + 1) % len(CornerCardinality)
                    if t.corners[previous_index] not in neighboring_corners:
                        neighboring_corners.append(t.corners[previous_index])
                    if t.corners[next_index] not in neighboring_corners:
                        neighboring_corners.append(t.corners[next_index])
        for nc in neighboring_corners:
            if nc != self and nc.ownership != 0:
                is_an_adjacent_corner_settled = True
                break
        return is_an_adjacent_corner_settled
