class Corner:
	def __init__(self, settlement = "none", ownership = 0):
		self.relational_id = ""
		self.edges         = []
		self.settlement    = settlement
		self.ownership     = ownership
	
	def addEdge(self, edge):
		if edge not in self.edges:
			self.edges.append(edge)

	def update(self, ownership):
		if ownership == self.ownership or self.ownership == 0:
			is_an_adjacent_corner_settled = False
			for e in self.edges:
				for c in e.corners:
					if c != self:
						if c.ownership != 0:
							is_an_adjacent_corner_settled = True

			if is_an_adjacent_corner_settled == False:				
				if self.settlement == "settlement":
					self.settlement = "city"
				elif self.settlement == "city":
					self.ownership = 0
					self.settlement = "none"
				else:
					self.ownership = ownership
					self.settlement = "settlement"
			else:
				print("Neighboring corners have settlements!")

	def str(self):
		return "Corner Settlement: " + self.settlement + ", Owned By:" + self.ownership