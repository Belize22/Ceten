from Corner import Corner

class Edge:
	def __init__(self, ownership="none", port="none"):
		self.relational_id = ""
		self.corners       = set([])
		self.ownership     = ownership
		self.port          = port

	def addCorners(self, corners, tile_id):
		for c in corners:
		    if (c.relational_id == "" and tile_id not in c.relational_id):
		    	c.relational_id += tile_id
		    elif (tile_id not in c.relational_id):
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