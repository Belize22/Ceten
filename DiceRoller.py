from Die import Die


class DieRoller:
    def __init__(self, num_dice=2, dice=None):
        if dice is None:
            dice = []
        self.dice = dice
        for i in range(num_dice):
            self.dice.append(Die(6))

    def roll_dice(self):
        ret = 0
        for d in self.dice:
            ret += d.roll()
        return ret
        
    def test(self):
        for x in range(6):
            print(str(self.roll_dice()))

