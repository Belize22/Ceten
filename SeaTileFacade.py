from TileFacade import TileFacade

import pygame


class SeaTileFacade(TileFacade):
    colour = {
        0: (91, 146, 176)
    }
    texture = {
        0: "./res/waterHex.gif"
    }

    def __init__(self, screen, tile, scale=1):
        super().__init__(screen, tile, scale)

    def set_colour(self):
        return SeaTileFacade.colour[0]

    def set_texture(self):
        return pygame.image.load(SeaTileFacade.texture[0])
