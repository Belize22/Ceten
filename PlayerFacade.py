from abc import ABC, abstractmethod

import pygame


class PlayerFacade(ABC):
    INVENTORY_ICON_SIZE = (16, 16)
    CARD_ICON_SIZE = (16, 20)

    resource_icons = {
        "lumber": "./res/icons/woodIcon.png",
        "wool": "./res/icons/sheepIcon.png",
        "grain": "./res/icons/wheatIcon.png",
        "brick": "./res/icons/clayIcon.png",
        "ore": "./res/icons/oreIcon.png"
    }

    resource_icon_order = [
        resource_icons.get("lumber"),
        resource_icons.get("wool"),
        resource_icons.get("grain"),
        resource_icons.get("brick"),
        resource_icons.get("ore")]

    def __init__(self, player, center, screen):
        self.player = player
        self.center = center
        self.screen = screen
        super().__init__()

    @abstractmethod
    def draw(self):
        pass

    def render_blit(self, string, point):
        font = pygame.font.Font(None, 24)
        text = font.render(string, 1, (10, 10, 10))
        self.screen.blit(text, point)
