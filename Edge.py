import re
from Corner import Corner

class Edge:
    def __init__(self, ownership="none", port="none"):
        self.relational_id = ""
        self.corners       = set([])
        self.ownership     = ownership
        self.port          = port

    def addCorners(self, corners, tile_id, at_perimeter):
        for c in corners:
            detect_num = re.search("([^0-9]*" + tile_id + "[^0-9]+)|([^0-9]+" + tile_id + "[^0-9]*)", c.relational_id)
            if (c.relational_id == "" and not detect_num):
                c.relational_id += tile_id
            elif (not detect_num):
                c.relational_id += ("-" + tile_id)
            self.corners.add(c)
            self.corners = set(self.corners)

    def hasCorner(self, corner):
        if (corner in self.corners):
            return "true"
        else:
            return "false"

    def getCorners(self):
        return corners