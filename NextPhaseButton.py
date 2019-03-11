import pygame
from Button import Button

class NextPhaseButton(Button):
	phases = {
		1  	: "Roll the Dice!",
		2  	: "Move the robber and rob a nearby settlement",
		3  	: "Select a Player, or the Bank, to trade with",
		4 	: "Build something from your Inventory",
		5 	: "End your Turn",
	}

	def __init__(self,position,dialog,screen):
		super().__init__(position,dialog,screen)
		self.phase_num = 1
		self.dialog = NextPhaseButton.phases[self.phase_num]
		self.center = position
		self.text_surf = None
		self.text_box = None
		self.draw()	

	def on_click(self):
		super().on_click()
		self.phase += 1

	def on_roll_robber(self):
		self.phase_num = 2
		self.dialog = NextPhaseButton.phases[self.phase_num]
		self.draw()
		print("Robbing the other players")

	def reset(self):
		self.phase_num = 1
		self.dialog = NextPhaseButton.phases[self.phase_num]
		self.draw()

	def on_roll_next(self):
		self.phase_num = 4
		self.dialog = NextPhaseButton.phases[self.phase_num]
		self.draw()
		print("next phase")
		
	def in_boundaries(self, position):
		return super().in_boundaries(position)
	
	def draw(self):
		pygame.draw.rect(self.screen, (228,205,180), ((0, self.center[1]),(self.screen.get_width(), self.screen.get_height() - self.center[1])))
		font = pygame.font.Font(None, 36)
		text = font.render(str(self.dialog), 1, (10, 10, 10))
		self.screen.blit(text, self.center)
