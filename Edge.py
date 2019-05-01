import re
from Corner import Corner


class Edge:
    def __init__(self, ownership="none", port="none"):
        self.relational_id = ""
        self.tiles = []
        self.corners = []
        self.ownership = ownership
        self.port = port

    def add_tile(self, tile):
        if tile not in self.tiles:
            self.tiles.append(tile)

    def add_corners(self, corners, tile_id):
        for c in corners:
            detect_num = re.search(
                "([^0-9]*" + tile_id + "[^0-9]+)|([^0-9]+" + tile_id
                + "[^0-9]*)", c.relational_id)
            if c.relational_id == "" and not detect_num:
                c.relational_id += tile_id
            elif not detect_num:
                c.relational_id += ("-" + tile_id)           
            if c not in self.corners:
                c.add_edge(self)
                self.corners.append(c)

    def has_corner(self, corner):
        if corner in self.corners:
            return True
        else:
            return False
