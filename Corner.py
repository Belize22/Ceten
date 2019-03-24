class Corner:
    def __init__(self, settlement="none", ownership=0):
        self.relational_id = ""
        self.edges = []
        self.settlement = settlement
        self.ownership = ownership

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)

    def update(self, ownership):
        if self.settlement == "settlement":
            self.settlement = "city"
        elif self.settlement == "none":
            self.ownership = ownership
            self.settlement = "settlement"

    def can_settlement_be_placed(self, ownership):
        can_settlement_be_placed = True
        if ownership == self.ownership or self.ownership == 0:
            is_an_adjacent_corner_settled = False
            for e in self.edges:
                for c in e.corners:
                    if c != self:
                        if c.ownership != 0:
                            is_an_adjacent_corner_settled = True
                            can_settlement_be_placed = False
            if is_an_adjacent_corner_settled:
                print("Neighboring corners have settlements!")
        else:
            can_settlement_be_placed = False
            print("You don't own this " + self.settlement + "!")
        return can_settlement_be_placed

    def str(self):
        return "Corner Settlement: " + self.settlement \
                + ", Owned By:" + str(self.ownership)
