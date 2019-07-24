from abc import ABC, abstractmethod

import pygame
import math


class TileFacade(ABC):
    def __init__(self, screen, tile, scale=1):
        self.tile = tile
        self.screen = screen
        self.center = self.set_center(self.screen, scale, self.tile.coordinate)
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

    @staticmethod
    def hex_pointlist_generator(scale, center):
        hex_pointlist = []
        for i in range(6):
            deg = 150.0 - i*60.0
            rad = math.pi / 180.0 * deg
            hex_pointlist.append(
                [center[0] + scale*math.cos(rad),
                 center[1] + scale*-math.sin(rad)])
        return hex_pointlist

    """set_center:
    The center point of the hexagon on the screen is determined by
    the tile's abstract coordinate. The tile with (0,0) as the abstract
    coordinate is at the center of the screen. Horizontal position
    is based on the x-coordinate and uses the hexagon's apothem as a
    basis. Vertical position is based on the y-coordinate and uses
    the hexagon's radius as a basis. An offset for vertical position
    exists for tiles with an even y-coordinate so that each tile
    can truly be adjacent to each other.
    """
    @staticmethod
    def set_center(screen, scale, tile_coordinate):
        center = [screen.get_width()*0.5,
                  screen.get_height()*0.5]
        radius = scale
        apothem = math.sqrt(radius**2 - (radius/2)**2)
        center[0] += 2*apothem*(tile_coordinate[0]) \
            + apothem*(tile_coordinate[1] % 2)
        center[1] += 1.5*radius*(tile_coordinate[1])
        return [int(center[0]), int(center[1])]

    @abstractmethod
    def set_colour(self):
        pass

    @abstractmethod
    def set_texture(self):
        pass

