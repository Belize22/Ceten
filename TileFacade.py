from abc import ABC, abstractmethod

import pygame
import math


class TileFacade(ABC):
    def __init__(self, screen, tile, scale=1):
        self.tile = tile
        self.screen = screen
        self.center = self.set_center(scale)
        self.points = self.hex_pointlist_generator(scale - 3, self.center)
        self.border_points = self.hex_pointlist_generator(scale, self.center)
        self.colour = self.set_colour()
        self.texture = self.set_texture()
        self.hex = None
        super().__init__()

    def draw(self):
        pygame.draw.polygon(
            self.screen, (0, 0, 0), self.border_points, 0)
        self.hex = pygame.draw.polygon(
            self.screen, self.colour, self.points, 0)
        self.texture = pygame.transform.scale(self.texture, self.hex.size)
        self.screen.blit(self.texture, self.hex)

    def hex_pointlist_generator(self, scale, center):
        hex_pointlist = []
        for i in range(6):
            deg = 60.0 * i - 30.0
            rad = math.pi / 180.0 * deg
            hex_pointlist.append(
                [center[0] + scale*math.cos(rad),
                 center[1] + scale*math.sin(rad)])
        return hex_pointlist

    def set_center(self, scale):
        center = [self.screen.get_width()*0.5,
                  self.screen.get_height()*0.5]
        radius = scale
        apothem = math.sqrt(radius**2 - (radius/2)**2)
        center[0] += 2*apothem*(self.tile.coordinate[0]) \
            + apothem*(self.tile.coordinate[1] % 2)
        center[1] += 1.5*radius*(self.tile.coordinate[1])
        print("Center: " + str(center[0]) + ", " + str(center[1]))
        return [int(center[0]), int(center[1])]

    @abstractmethod
    def set_colour(self):
        pass

    @abstractmethod
    def set_texture(self):
        pass

