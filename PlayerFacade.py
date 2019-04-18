from Player import Player
import pygame


class PlayerFacade:
    colour = {
        "WHITE": (255, 255, 255),
        "YELLOW": (255, 209, 102),
        "BLUE": (168, 168, 255),
        "RED": (255, 168, 168),
    }
    resource_icons = {
        "lumber": "./res/icons/woodIcon.png",
        "wool": "./res/icons/sheepIcon.png",
        "grain": "./res/icons/wheatIcon.png",
        "brick": "./res/icons/clayIcon.png",
        "ore": "./res/icons/oreIcon.png"
    }
    game_piece_icons = {
        "road": "./res/icons/roadIcon.png",
        "settlement": "./res/icons/settlementIcon.png",
        "city": "./res/icons/cityIcon.png"
    }
    development_card_icons = {
        "victory": "./res/icons/victoryIcon.png",
        "knight": "./res/icons/knightIcon.png",
        "monopoly": "./res/icons/monopolyIcon.png",
        "year_of_plenty": "./res/icons/yearOfPlentyIcon.png",
        "road_building": "./res/icons/roadBuildingIcon.png",
        "face_down": "./res/icons/genericCardIcon.png",
    }

    player_to_colour_mapping = [colour.get("WHITE"),
                                colour.get("YELLOW"),
                                colour.get("BLUE"),
                                colour.get("RED")]

    resource_icon_order = [resource_icons.get("lumber"),
                           resource_icons.get("wool"),
                           resource_icons.get("grain"),
                           resource_icons.get("brick"),
                           resource_icons.get("ore")]
    game_piece_icon_order = [game_piece_icons.get("road"),
                             game_piece_icons.get("settlement"),
                             game_piece_icons.get("city")]
    development_card_icon_order = [development_card_icons.get("victory"),
                                   development_card_icons.get("knight"),
                                   development_card_icons.get("monopoly"),
                                   development_card_icons.get("year_of_plenty"),
                                   development_card_icons.get("road_building")]
    public_development_card_icon_order = [development_card_icons.get("face_down"),
                                          development_card_icons.get("knight")]

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
        shift_x = 17.5
        shift_y = 25
        x = 2
        y = 25
        for i in range(0, len(self.resource_icon_order)):
            resource_rect = pygame.draw.rect(self.screen, (0, 0, 0),
                                             ((self.screen.get_width()*0.8 + x,
                                               self.center[1] + y),
                                             (16, 16)), 0)
            resource_image = pygame.image.load(self.resource_icon_order[i])
            resource_texture = pygame.transform.scale(resource_image, resource_rect.size)
            self.screen.blit(resource_texture, resource_rect)
            x += shift_x
            self.__render_blit(str(self.player.resource_bank.resources[i]),
                               (self.screen.get_width() * 0.8 + x,
                                self.center[1] + y))
            x += shift_x
        x = 2
        y += shift_y
        for i in range(0, len(self.game_piece_icon_order)):
            game_piece_rect = pygame.draw.rect(self.screen, (0, 0, 0),
                                               ((self.screen.get_width()*0.8 + x,
                                                 self.center[1] + y),
                                                (16, 16)), 0)
            game_piece_image = pygame.image.load(self.game_piece_icon_order[i])
            game_piece_texture = pygame.transform.scale(game_piece_image, game_piece_rect.size)
            x += shift_x
            self.screen.blit(game_piece_texture, game_piece_rect)
            self.__render_blit(str(self.player.game_piece_bank.game_pieces[i]),
                           (self.screen.get_width()*0.8 + x,
                            self.center[1] + y))
            x += shift_x
        x = 2
        y += shift_y
        for i in range(0, len(self.development_card_icon_order)):
            development_card_rect = pygame.draw.rect(self.screen, (0, 0, 0),
                                               ((self.screen.get_width() * 0.8 + x,
                                                 self.center[1] + y),
                                                (16, 20)), 0)
            development_card_image = pygame.image.load(self.development_card_icon_order[i])
            development_card_texture = pygame.transform.scale(development_card_image,
                                                              development_card_rect.size)
            x += shift_x
            self.screen.blit(development_card_texture, development_card_rect)
            x += shift_x

    def draw_public(self):
        pygame.draw.rect(self.screen, self.player_to_colour_mapping[self.player.id-1],
                         ((0, self.screen.get_height()*0.25*(self.player.id-1)),
                          (self.screen.get_width()*0.2,
                           self.screen.get_height()*0.25)),
                         0)
        shift_x = 17.5
        shift_y = 20
        x = 2
        y = 20
        for i in range(0, len(self.resource_icon_order)):
            resource_rect = pygame.draw.rect(self.screen, (0, 0, 0),
                                             ((x,
                                               self.center[1]
                                               + self.screen.get_height()*0.25*(self.player.id-1)
                                               + y),
                                             (16, 16)), 0)
            resource_image = pygame.image.load(self.resource_icon_order[i])
            resource_texture = pygame.transform.scale(resource_image, resource_rect.size)
            self.screen.blit(resource_texture, resource_rect)
            x += shift_x
            self.__render_blit(str(self.player.resource_bank.resources[i]),
                               (x,
                                self.center[1]+self.screen.get_height()*0.25*(self.player.id-1)+y))
            x += shift_x
        self.__render_blit(self.player.name_str(),
                           [0, self.center[1] + self.screen.get_height()*0.25*(self.player.id-1)])
        x = 2
        y += shift_y
        for i in range(0, len(self.public_development_card_icon_order)):
            development_card_rect = pygame.draw.rect(self.screen, (0, 0, 0),
                                                     ((x, self.center[1] +
                                                       self.screen.get_height()*0.25
                                                       * (self.player.id-1) + y),
                                             (16, 20)), 0)
            development_card_image = pygame.image.load(self.public_development_card_icon_order[i])
            development_card_texture = pygame.transform.scale(development_card_image,
                                                              development_card_rect.size)
            self.screen.blit(development_card_texture, development_card_rect)
            x += shift_x
            x += shift_x
        self.__render_blit(self.player.name_str(), [0, self.center[1]
                                                    + self.screen.get_height()*0.25
                                                    * (self.player.id-1)])

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

    '''
    TO-DO: Make a separate function to reduce duplication coming from
    the loops responsible for generating icons and quantities associated
    with them.
    Note: Can ONLY be done once Development Cards are implemented. Inconsistencies between
    development card icons and all other icons makes it difficult to implement this function
    for the time being.
    '''
    # def render_inventory(self, rect, inventory_mapping, shift_x):
