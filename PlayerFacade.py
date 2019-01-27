from Player import Player
import pygame

class PlayerFacade:

	def __init__(self, player, center, screen):
		self.player = player
		self.center = center
		self.screen = screen
	
	def draw(self):
		pygame.draw.rect(self.screen,
				(228, 205, 180), 
				((0, self.center[1]),(self.screen.get_width(), self.screen.get_height() - self.center[1])), 
				0)
		self.__render_blit(self.player.name_str(),[0, self.center[1]])
		shift_x = 200
		self.__render_blit("Resources",[shift_x, self.center[1]])
		shift_y = 20
		x = shift_x
		y = self.center[1] + shift_y
		for s in self.player.res_str_list():
			self.__render_blit(s,[x, y])
			y += shift_y
		x+=shift_x
		y = self.center[1]
		self.__render_blit("Inventory",[x, self.center[1]])
		y+= shift_y
		for s in self.player.piece_str_list():
			self.__render_blit(s,[x,y])	
			y += shift_y


	def gather(self, res_dict):
		self.player.num_wool 	+= res_dict["wool"]	
		self.player.num_grain 	+= res_dict["grain"]	
		self.player.num_brick 	+= res_dict["brick"]	
		self.player.num_ore 	+= res_dict["ore"]	
		self.player.num_lumber  += res_dict["lumber"]
		print(self.player.str())	

	def __render_blit(self, string, point):
		font = pygame.font.Font(None, 24)
		text = font.render(string, 1, (10,10,10))
		self.screen.blit( text, point)
