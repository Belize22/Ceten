import pygame


class EdgeFacade:
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

    def __init__(self, line_endpoints, edge, screen):
        self.line_endpoints = line_endpoints
        self.edge = edge
        self.screen = screen
        self.line = None
        self.draw()

    def update(self, player):
        self.edge.update(player.id)
        self.draw()

    def draw(self):
        self.line = pygame.draw.line(
            self.screen,
            self.player_to_colour_mapping[self.edge.ownership],
            self.line_endpoints[0], self.line_endpoints[1], 5)
