from TileFacade import TileFacade
from PortType import PortType

import pygame


class SeaTileFacade(TileFacade):
    colour = {
        PortType.LUMBER.value: (0, 51, 0),
        PortType.WOOL.value: (77, 255, 77),
        PortType.GRAIN.value: (255, 255, 0),
        PortType.BRICK.value: (255, 0, 0),
        PortType.ORE.value: (102, 102, 102)
    }

    def __init__(self, screen, tile, scale=1):
        super().__init__(screen, tile, scale)

    def set_colour(self):
        for i in range(0, len(self.tile.edges)):
            if self.tile.edges[i].port is not None:
                if self.tile.edges[i].port is not PortType.STANDARD.value:
                    return SeaTileFacade.colour[self.tile.edges[i].port]
        return 91, 146, 176 # Color of the water

    def set_texture(self):
        for i in range (0, len(self.tile.edges)):
            if self.tile.edges[i].port is not None:
                if self.tile.edges[i].port is PortType.STANDARD.value:
                    return pygame.image.load(
                        "./res/miscPort" + str(i) + ".gif")
                else:
                    return pygame.image.load(
                        "./res/port" + str(i) + ".gif")
        return pygame.image.load("./res/waterHex.gif")

