class Corner:
	def __init__(self, settlement = "none", ownership = 0):
		self.relational_id = ""
		self.edges         = []
		self.settlement    = settlement
		self.ownership     = ownership
	
	def addEdge(self, edge):
		if edge not in self.edges:
			self.edges.append(edge)

	def str(self):
		return "Corner Settlement: " + self.settlement + ", Owned By:" + self.ownership