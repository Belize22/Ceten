from SettlementLevel import SettlementLevel

import pygame


class CornerFacade:
    colour = {
        "GREY": (128, 128, 128),
        "WHITE": (225, 225, 225),
        "YELLOW": (255, 180, 0),
        "BLUE": (0, 0, 255),
        "RED": (255, 0, 0),
        "BLACK": (0, 0, 0)
    }

    player_to_colour_mapping = [
        colour.get("GREY"),
        colour.get("WHITE"),
        colour.get("YELLOW"),
        colour.get("BLUE"),
        colour.get("RED")]

    def __init__(self, position, corner, screen, radius):
        self.center = position
        self.corner = corner
        self.screen = screen
        self.radius = int(radius)
        self.circle = None
        self.draw()

    def update(self, player):
        self.corner.update(player.id)
        self.draw()

    def draw(self):
        self.circle = pygame.draw.circle(
            self.screen,
            self.player_to_colour_mapping[self.corner.ownership],
            self.center, self.radius, 0)
        if self.corner.settlement == SettlementLevel.CITY.value:
            self.circle = pygame.draw.circle(
                self.screen, self.colour.get("BLACK"), self.center,
                round(self.radius/2), 1)
        self.circle = pygame.draw.circle(
            self.screen, self.colour.get("BLACK"), self.center, self.radius, 2)
