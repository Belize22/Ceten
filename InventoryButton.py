from Button import Button

import pygame
import math


class InventoryButton(Button):
    # Triangle, then circle respectively.
    DISABLED_COLOR_SCHEME = [(80, 80, 80), (150, 150, 150)]
    ENABLED_COLOR_SCHEME = [(0, 0, 0), (180, 180, 180)]

    def __init__(self, screen, position, orientation):
        super().__init__(screen, position)
        self.triangle_pointlist = []
        self.line_length = 5
        if orientation == "up":
            degree = math.pi/2    # 90 degrees in unit circle.
        else:
            degree = 3*math.pi/2  # 270 (-90) degrees in unit circle.
        for i in range(0, 3):
            self.triangle_pointlist.append(
                [self.position[0]+int(self.line_length*math.cos(degree)),
                 self.position[1]+int(self.line_length*-math.sin(degree))])
            degree += 2*math.pi/3

    def draw(self):
        if self.enabled:
            current_color_scheme = self.ENABLED_COLOR_SCHEME
        else:
            current_color_scheme = self.DISABLED_COLOR_SCHEME
        pygame.draw.circle(
            self.screen, current_color_scheme[1], self.position,
            int(self.line_length*2))
        pygame.draw.polygon(
            self.screen, current_color_scheme[0], self.triangle_pointlist, 0)

    """in_boundaries:
    Determines if the button was clicked by checking if the distance
    between where the user clicked and the center of the button is
    less than or equal to the button's radius.
    """
    def in_boundaries(self, position):
        if ((math.sqrt((position[0]-self.position[0])**2
                       + (position[1]-self.position[1])**2))
                < self.line_length * 2):
            return True
        return False




