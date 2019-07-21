class Edge:
    def __init__(self, ownership=0):
        self.tiles = []
        self.ownership = ownership
        self.port = None

    def update(self, ownership):
        self.ownership = ownership

