from Player import Player
from InventoryPanel import InventoryPanel
from InventoryButtonPanel import InventoryButtonPanel
from InventoryButton import InventoryButton
import pygame


class PlayerFacade:
    INVENTORY_ICON_SIZE = (16, 16)
    CARD_ICON_SIZE = (16, 20)

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

    player_to_colour_mapping = [
        colour.get("WHITE"),
        colour.get("YELLOW"),
        colour.get("BLUE"),
        colour.get("RED")]
    resource_icon_order = [
        resource_icons.get("lumber"),
        resource_icons.get("wool"),
        resource_icons.get("grain"),
        resource_icons.get("brick"),
        resource_icons.get("ore")]
    game_piece_icon_order = [
        game_piece_icons.get("road"),
        game_piece_icons.get("settlement"),
        game_piece_icons.get("city")]
    development_card_icon_order = [
        development_card_icons.get("victory"),
        development_card_icons.get("knight"),
        development_card_icons.get("monopoly"),
        development_card_icons.get("year_of_plenty"),
        development_card_icons.get("road_building")]
    public_development_card_icon_order = [
        development_card_icons.get("face_down"),
        development_card_icons.get("knight")]

    def __init__(self, player, center, screen):
        self.player = player
        self.center = center
        self.screen = screen
        self.private_resource_panel = InventoryPanel(
            (self.screen.get_width()*0.8 + 2, self.center[1] + 50),
            self.screen, self.player.resource_bank.resources,
            self.resource_icon_order, self.INVENTORY_ICON_SIZE)
        self.private_resource_incrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 35),
            len(self.resource_icon_order), "up")
        self.private_resource_decrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 80),
            len(self.resource_icon_order), "down")
        self.public_resource_panel = None
        self.game_piece_panel = InventoryPanel(
            (self.screen.get_width()*0.8 + 2, self.center[1] + 100),
            self.screen, self.player.game_piece_bank.game_pieces,
            self.game_piece_icon_order, self.INVENTORY_ICON_SIZE)
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.development_card_panel = InventoryPanel(
            (self.screen.get_width()*0.8 + 2, self.center[1] + 125),
            self.screen, [0, 0, 0, 0, 0],
            self.development_card_icon_order, self.CARD_ICON_SIZE)
        self.public_development_card_panel = None
        self.inventory_button_test = InventoryButton(
            self.screen,
            (int(self.screen.get_width()*0.8) + 45, self.center[1] + 35), "up")

    def initialize_public_panels(self):
        self.public_resource_panel = InventoryPanel(
                (2, self.center[1]
                 + self.screen.get_height()*0.25
                 * (self.player.turn_priority - 1) + 25), self.screen,
                self.player.resource_bank.resources,
                self.resource_icon_order, self.INVENTORY_ICON_SIZE)
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.public_development_card_panel = InventoryPanel(
                (107, self.center[1]
                 + self.screen.get_height()*0.25
                 * (self.player.turn_priority - 1)), self.screen,
                [0, 0],
                self.public_development_card_icon_order, self.CARD_ICON_SIZE)

    def draw(self):
        pygame.draw.rect(
            self.screen, (228, 205, 180),
            ((self.screen.get_width()*0.8, self.center[1]),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.__render_blit(
            self.player.name_str(),
            [self.screen.get_width()*0.8, self.center[1]])
        self.private_resource_incrementers.draw()
        self.private_resource_decrementers.draw()
        self.private_resource_panel.draw()
        self.game_piece_panel.draw()
        self.development_card_panel.draw()

    def draw_public(self):
        pygame.draw.rect(
            self.screen,
            self.player_to_colour_mapping[self.player.id-1],
            ((0, self.screen.get_height()*0.25*(self.player.turn_priority-1)),
             (self.screen.get_width()*0.2,
              self.screen.get_height()*0.25)), 0)
        self.__render_blit(
            self.player.name_str(),
            [0, self.center[1]
             + self.screen.get_height()*0.25*(self.player.turn_priority-1)])
        self.public_resource_panel.draw()
        self.public_development_card_panel.draw()

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
