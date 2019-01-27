from Die import Die

class DieRoller:
	def __init__(self, numDice = 2, dice = []):
		self.dice = dice
		for i in range(2):
			self.dice.append(Die(6))

	def roll_dice(self):
		ret = 0
		for d in self.dice:
			ret+=d.roll()
		return ret
	def test(self):
		for x in range(6):
			print (str(self.roll_dice()))

