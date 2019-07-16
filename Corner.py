class Corner:
    def __init__(self, settlement="none", ownership=0):
        self.tiles = []
        self.settlement = settlement
        self.ownership = ownership

    # TODO: Replace logic with increment by implementing enum
    def update(self, ownership):
        if self.settlement == "settlement":
            self.settlement = "city"
        elif self.settlement == "none":
            self.ownership = ownership
            self.settlement = "settlement"

    def does_corner_belong_to_a_player(self, ownership):
        does_corner_have_ownership = False
        if ownership == self.ownership or self.ownership == 0:
            does_corner_have_ownership = True
        return does_corner_have_ownership

    def are_neighboring_corners_settled(self):
        is_an_adjacent_corner_settled = False
        for e in self.edges:
            for c in e.corners:
                if c != self:
                    if c.ownership != 0:
                        is_an_adjacent_corner_settled = True
        return is_an_adjacent_corner_settled
