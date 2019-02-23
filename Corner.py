class Corner:
	def __init__(self, settlement = "none", ownership = "none"):
		self.relational_id = ""
		self.settlement    = settlement
		self.ownership     = ownership

	def addCorner(self, corner):
		self.corners.append(corner)

	def str(self):
		return "Corner Settlement: " + self.settlement + ", Owned By:" + self.ownership