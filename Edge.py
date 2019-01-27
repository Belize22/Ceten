from Corner import Corner

class Edge:
	def __init__(self, ownership="none", port="none"):
		self.corners = set([])
		self.ownership = ownership
		self.port = port

	def addCorner(self, corner):
		self.corners.add(corner)
		self.corners = set(self.corners)

	def getCorners(self):
		return corners