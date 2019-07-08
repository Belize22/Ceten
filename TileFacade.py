from SeaTile import SeaTile
from ResourceType import ResourceType

import pygame
import math


class TileFacade:
    colour = {
        ResourceType.LUMBER.value: (0, 51, 0),
        ResourceType.WOOL.value: (77, 255, 77),
        ResourceType.GRAIN.value: (255, 255, 0),
        ResourceType.BRICK.value: (255, 0, 0),
        ResourceType.ORE.value: (102, 102, 102),
        ResourceType.DESERT.value: (255, 255, 255),
        6: (91, 146, 176)
    }
    texture = {
        ResourceType.LUMBER.value: "./res/woodHex.gif",
        ResourceType.WOOL.value: "./res/sheepHex.gif",
        ResourceType.GRAIN.value: "./res/wheatHex.gif",
        ResourceType.BRICK.value: "./res/clayHex.gif",
        ResourceType.ORE.value: "./res/oreHex.gif",
        ResourceType.DESERT.value: "./res/desertHex.gif",
        6: "./res/waterHex.gif"  # Until enums for water tile are defined
    }

    def __init__(self, screen, tile, scale=1,
                 port_direction=-1):
        self.tile = tile
        self.screen = screen
        self.center = self.set_center(scale)
        self.points = self.hex_pointlist_generator(scale - 3, self.center)
        self.border_points = self.hex_pointlist_generator(scale, self.center)
        self.colour = self.set_colour()
        self.port_direction = port_direction
        self.texture = self.set_texture()
        self.text = ""
        self.rect = None

    def draw(self):
        pygame.draw.polygon(
            self.screen, (0, 0, 0), self.border_points, 0)
        self.rect = pygame.draw.polygon(
            self.screen, self.colour, self.points, 0)
        self.texture = pygame.transform.scale(self.texture, self.rect.size)
        self.screen.blit(self.texture, self.rect)

        if not isinstance(self.tile, SeaTile):
            if str(self.tile.activation_value) != "0" or self.tile.robber:
                self.text = self.set_activation_value(
                    str(self.tile.activation_value))
                color = (228, 205, 180)
                if self.tile.robber:
                    color = (27, 50, 75)
                pygame.draw.circle(self.screen, color, self.centre, 15, 0)
                self.screen.blit(
                    self.text, [self.centre[0] - 11, self.centre[1] - 8])

    def hex_pointlist_generator(self, scale, center):
        hex_pointlist = []
        for i in range(6):
            deg = 60.0 * i - 30.0
            rad = math.pi / 180.0 * deg
            hex_pointlist.append(
                [center[0] + scale*math.cos(rad),
                 center[1] + scale*math.sin(rad)])
        return hex_pointlist

    def set_activation_value(self, activation_value):
        font = pygame.font.Font(None, 24)
        color = (10, 10, 10)
        if activation_value == "6" or activation_value == "8":
            color = (255, 0, 0)
        if self.tile.robber:
            activation_value = "R"
            color = (255, 255, 255)
        return font.render(activation_value, 1, color)

    def set_center(self, scale):
        center = [self.screen.get_width()*0.5,
                  self.screen.get_height()*0.5]
        radius = scale
        apothem = math.sqrt(radius**2 - (radius/2)**2)
        center[0] += 2*apothem*(self.tile.coordinates[0]) \
            + apothem*(self.tile.coordinates[1] % 2)
        center[1] += 1.5*radius*(self.tile.coordinates[1])
        print("Center: " + str(center[0]) + ", " + str(center[1]))
        return center

    def set_colour(self):
        if isinstance(self.tile, SeaTile):
            return TileFacade.colour[6]
        else:
            return TileFacade.colour[self.tile.resource]

    def set_texture(self):
        if isinstance(self.tile, SeaTile):
            return pygame.image.load(TileFacade.texture[6])
        else:
            return pygame.image.load(TileFacade.texture[self.tile.resource])

    def set_robber(self, flag):
        self.tile.robber = flag
