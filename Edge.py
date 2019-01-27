from Corner import Corner

class Edge:
	def __init__(self, corners = [], ownership="none", port="none"):
		self.corners = corners
		self.ownership = ownership
		self.port = port

	def getCorners(self):
		return corners