from TileFacade import TileFacade
from ResourceType import ResourceType

import pygame


class LandTileFacade(TileFacade):
    colour = {
        ResourceType.LUMBER.value: (0, 51, 0),
        ResourceType.WOOL.value: (77, 255, 77),
        ResourceType.GRAIN.value: (255, 255, 0),
        ResourceType.BRICK.value: (255, 0, 0),
        ResourceType.ORE.value: (102, 102, 102),
        ResourceType.DESERT.value: (255, 255, 255)
    }
    texture = {
        ResourceType.LUMBER.value: "./res/woodHex.gif",
        ResourceType.WOOL.value: "./res/sheepHex.gif",
        ResourceType.GRAIN.value: "./res/wheatHex.gif",
        ResourceType.BRICK.value: "./res/clayHex.gif",
        ResourceType.ORE.value: "./res/oreHex.gif",
        ResourceType.DESERT.value: "./res/desertHex.gif"
    }

    def __init__(self, screen, tile, scale=1):
        super().__init__(screen, tile, scale)
        self.text = ""
        self.text_width = 0
        self.text_height = 0

    def draw(self):
        super().draw()

        if (self.tile.resource != ResourceType.DESERT.value
                or self.tile.robber):
            self.text = self.set_activation_value(
                str(self.tile.activation_value))
            self.render_token()

    def set_activation_value(self, activation_value):
        font = pygame.font.Font(None, 24)
        color = (10, 10, 10)
        if activation_value == "6" or activation_value == "8":
            color = (255, 0, 0)
        if self.tile.robber:
            activation_value = "R"
            color = (255, 255, 255)
        self.text_width, self.text_height = font.size(
            str(activation_value))
        return font.render(activation_value, 1, color)

    def render_token(self):
        color = (228, 205, 180)
        if self.tile.robber:
            color = (27, 50, 75)
        pygame.draw.circle(self.screen, color, self.center, 15, 0)
        self.screen.blit(
            self.text, [self.center[0] - self.text_width*0.5,
                        self.center[1] - self.text_height*0.5])

    def set_colour(self):
        return LandTileFacade.colour[self.tile.resource]

    def set_texture(self):
        return pygame.image.load(LandTileFacade.texture[self.tile.resource])

    def set_robber(self, flag):
        self.tile.robber = flag
