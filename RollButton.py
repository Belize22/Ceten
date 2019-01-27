import pygame
from Button import Button
from DiceRoller import DieRoller

class RollButton(Button):
	def __init__(self, position, dialog, screen, num_dice = 2):
		super().__init__(position, dialog, screen)
		self.dr = DieRoller(num_dice)
		self.center = (position[0], position[1] + 60)
		self.roll = 0
	def on_click(self):
		super().on_click()
		self.roll = self.__roll_dice()
		self.draw()
	def on_roll(self):
		if self.roll == 7:
			return True
		return False
	def __roll_dice(self):
		roll = self.dr.roll_dice()
		print("Current Role: " + str(roll))
		return roll
	def in_boundaries(self,position):
		return super().in_boundaries(position)
	def draw(self):
		pygame.draw.circle(self.screen, (228, 205, 180), self.center, 30, 0)
		font = pygame.font.Font(None, 36)
		text = font.render(str(self.roll), 1, (10,10,10))
		self.screen.blit(text,[self.center[0] - 11, self.center[1] - 8])