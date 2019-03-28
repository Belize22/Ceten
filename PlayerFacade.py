from Player import Player
import pygame


class PlayerFacade:
    colour = {
        "WHITE": (255, 255, 255),
        "YELLOW": (255, 209, 102),
        "BLUE": (168, 168, 255),
        "RED": (255, 168, 168),
    }

    player_to_colour_mapping = [colour.get("WHITE"),
                                colour.get("YELLOW"),
                                colour.get("BLUE"),
                                colour.get("RED")]

    def __init__(self, player, center, screen):
        self.player = player
        self.center = center
        self.screen = screen
    
    def draw(self):
        pygame.draw.rect(self.screen, (228, 205, 180),
                         ((self.screen.get_width()*0.8, self.center[1]),
                          (self.screen.get_width()*0.2,
                           self.screen.get_height()*0.5)),
                         0)
        self.__render_blit(self.player.name_str(), [self.screen.get_width()*0.8, self.center[1]])
        shift_x = 20
        self.__render_blit("Resources:", [self.screen.get_width()*0.8, self.center[1]+25])
        shift_y = 20
        x = self.screen.get_width()*0.8
        y = shift_y+25
        for s in self.player.res_str_list():
            self.__render_blit(s, [x, y])
            y += shift_y
        y += shift_x
        self.__render_blit("Inventory:", [x, y])
        y += 20
        for s in self.player.piece_str_list():
            self.__render_blit(s, [x, y])
            y += shift_y

    def draw_public(self):
        pygame.draw.rect(self.screen, self.player_to_colour_mapping[self.player.id-1],
                         ((0, self.screen.get_height()*0.25*(self.player.id-1)),
                          (self.screen.get_width()*0.2,
                           self.screen.get_height()*0.25)),
                         0)
        self.__render_blit(self.player.name_str(), [0, self.center[1]+self.screen.get_height()*0.25*(self.player.id-1)])
        shift_x = 20
        self.__render_blit("Resources:", [0, self.center[1]+20+self.screen.get_height()*0.25*(self.player.id-1)])
        shift_y = 15
        x = 0
        y = shift_y+20++self.screen.get_height()*0.25*(self.player.id-1)
        for s in self.player.res_str_list():
            self.__render_blit(s, [x, y])
            y += shift_y

    def gather(self, res_dict):
        self.player.num_wool += res_dict["wool"]	
        self.player.num_grain += res_dict["grain"]	
        self.player.num_brick += res_dict["brick"]	
        self.player.num_ore += res_dict["ore"]	
        self.player.num_lumber += res_dict["lumber"]
        print(self.player.str())	

    def __render_blit(self, string, point):
        font = pygame.font.Font(None, 24)
        text = font.render(string, 1, (10, 10, 10))
        self.screen.blit(text, point)
