from PlayerFacade import PlayerFacade
from InventoryPanel import InventoryPanel
import pygame


class PublicPlayerFacade(PlayerFacade):
    colour = {
        "WHITE": (255, 255, 255),
        "YELLOW": (255, 209, 102),
        "BLUE": (168, 168, 255),
        "RED": (255, 168, 168),
    }
    development_card_icons = {
        "face_down": "./res/icons/genericCardIcon.png",
        "knight": "./res/icons/knightIcon.png"
    }

    player_to_colour_mapping = [
        colour.get("WHITE"),
        colour.get("YELLOW"),
        colour.get("BLUE"),
        colour.get("RED")]
    development_card_icon_order = [
        development_card_icons.get("face_down"),
        development_card_icons.get("knight")]

    def __init__(self, player, center, screen):
        super().__init__(player, center, screen)
        self.resource_panel = None
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.development_card_panel = None

    def initialize_panels(self):
        self.resource_panel = InventoryPanel(
            self.screen,
            (2, self.center[1] + self.screen.get_height()*0.25
             * (self.player.turn_priority - 1) + 25),
            self.player.resource_bank.resources, self.resource_icon_order,
            self.INVENTORY_ICON_SIZE)
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.development_card_panel = InventoryPanel(
            self.screen,
            (107, self.center[1] + self.screen.get_height()*0.25
             * (self.player.turn_priority - 1)), [0, 0],
            self.development_card_icon_order, self.CARD_ICON_SIZE)

    def draw(self):
        pygame.draw.rect(
            self.screen,
            self.player_to_colour_mapping[self.player.id - 1],
            ((0, self.screen.get_height()*0.25*(
                        self.player.turn_priority - 1)),
             (self.screen.get_width()*0.2,
              self.screen.get_height()*0.25)), 0)
        self.render_text(
            self.player.retrieve_player_name(),
            [0, self.center[1]
             + self.screen.get_height()*0.25*(
                         self.player.turn_priority - 1)])
        self.resource_panel.draw()
        self.development_card_panel.draw()
