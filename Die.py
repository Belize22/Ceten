import random

class Die:
	roll_value = 0
	sides = 0

	def __init__(self,sides = 6):
		self.sides = sides
		
	def roll(self):
		roll_value = random.randint(1,self.sides)
		return roll_value 

