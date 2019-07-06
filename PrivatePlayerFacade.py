from PlayerFacade import PlayerFacade
from InventoryPanel import InventoryPanel
from InventoryButtonPanel import InventoryButtonPanel
from SubmitButton import SubmitButton

import pygame


class PrivatePlayerFacade(PlayerFacade):
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

    def __init__(self, player, center, screen):
        super().__init__(player, center, screen)
        self.resource_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 50),
            self.player.resource_bank.resources, self.resource_icon_order,
            self.INVENTORY_ICON_SIZE)
        self.resource_incrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 35),
            len(self.resource_icon_order), "up")
        self.resource_decrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 80),
            len(self.resource_icon_order), "down")
        self.game_piece_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 150),
            self.player.game_piece_bank.game_pieces,
            self.game_piece_icon_order, self.INVENTORY_ICON_SIZE)
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.development_card_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 175),
            [0, 0, 0, 0, 0],
            self.development_card_icon_order, self.CARD_ICON_SIZE)
        self.resource_submit_button = SubmitButton(
            self.screen, (int(self.screen.get_width()*0.9), 115), "Submit")

    def draw(self):
        pygame.draw.rect(
            self.screen, (228, 205, 180),
            ((self.screen.get_width()*0.8, self.center[1]),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.render_text(
            self.player.retrieve_player_name(),
            [self.screen.get_width()*0.8, self.center[1]])

        self.resource_incrementers.draw()
        self.resource_decrementers.draw()
        self.resource_panel.draw()
        self.game_piece_panel.draw()
        self.development_card_panel.draw()
        self.resource_submit_button.draw()

    def get_player(self):
        return self.player

    def set_next_player(self, player):
        self.player = player
        self.resource_panel.update(player.resource_bank.resources)
        self.game_piece_panel.update(player.game_piece_bank.game_pieces)
