from Dice import Dice


class DieRoller:
    DICE_FACES = 6

    def __init__(self, num_dice=2, dice=None):
        if dice is None:
            dice = []
        self.dice = dice
        for i in range(num_dice):
            self.dice.append(Dice(self.DICE_FACES))

    def roll_dice(self):
        total = 0
        for d in self.dice:
            total += d.roll()
        return total
        
    def test(self):
        for x in range(self.DICE_FACES):
            print(str(self.roll_dice()))

