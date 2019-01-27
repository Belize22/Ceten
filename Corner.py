class Corner:
	def __init__(self, settlement = "none", ownership = "none"):
		self.settlement = settlement
		self.ownership = ownership

	def str(self):
		return "Corner Settlement: " + self.settlement + ", Owned By:" + self.ownership