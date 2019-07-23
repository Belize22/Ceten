from Button import Button

import pygame


class SubmitButton(Button):
    # Button color, text color, border color respectively.
    DISABLED_COLOR_SCHEME = [(155, 155, 155), (75, 75, 75), (10, 10, 10)]
    ENABLED_COLOR_SCHEME = [(155, 155, 255), (10, 10, 10), (10, 10, 10)]

    def __init__(self, screen, position, dialog):
        super().__init__(screen, position)
        self.dialog = ""
        self.text_surf = None
        self.text_box = None
        self.font = pygame.font.Font(None, 36)
        self.update(dialog)

    def draw(self):
        if self.enabled:
            current_color_scheme = self.ENABLED_COLOR_SCHEME
        else:
            current_color_scheme = self.DISABLED_COLOR_SCHEME
        (self.text_surf, self.text_box) = self.text_objects(
            self.dialog, self.font, current_color_scheme[1])
        self.text_box.center = self.position
        font_size = self.font.size(self.dialog)
        pygame.draw.rect(
            self.screen, current_color_scheme[0],
            ((self.position[0]-font_size[0]/2,
              self.position[1]-font_size[1]/2), font_size), 0)
        pygame.draw.rect(
            self.screen, current_color_scheme[2],
            ((self.position[0]-font_size[0]/2,
              self.position[1]-font_size[1]/2), font_size), 2)
        self.screen.blit(self.text_surf, self.text_box)

    def in_boundaries(self, position):
        return self.text_box.collidepoint(position) and self.enabled

    def update(self, dialog):
        self.dialog = dialog
        self.draw()

    def text_objects(self, text, font, text_color):
        text_surface = font.render(text, 1, text_color)
        return text_surface, text_surface.get_rect()
