import random


class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        
    def roll(self):
        roll_value = random.randint(1, self.sides)
        return roll_value 

