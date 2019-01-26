from Die import Die

class DieRoller:
	dice = []
	def __init__(self, numDice = 2):
		for i in range(2):
			self.dice.append(Die(6))

	def roll_dice(self):
		ret = 0
		for d in self.dice:
			ret+=d.roll()
		return ret
	def __test__(self):
		for x in range(6):
			print self.roll_dice()	
