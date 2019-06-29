import pygame


class SubmitButton:
    BUTTON_COLOR = (155, 155, 255)
    TEXT_COLOR = (10, 10, 10)
    BORDER_COLOR = TEXT_COLOR

    def __init__(self, screen, position, dialog):
        self.screen = screen
        self.position = position
        self.dialog = ""
        self.text_surf = None
        self.text_box = None
        self.font = pygame.font.Font(None, 36)
        self.update(dialog)

    def draw(self):
        (self.text_surf, self.text_box) = self.text_objects(
            self.dialog, self.font)
        self.text_box.center = self.position
        font_size = self.font.size(self.dialog)
        pygame.draw.rect(
            self.screen, self.BUTTON_COLOR,
            ((self.position[0]-font_size[0]/2,
              self.position[1]-font_size[1]/2), font_size), 0)
        pygame.draw.rect(
            self.screen, self.BORDER_COLOR,
            ((self.position[0]-font_size[0]/2,
              self.position[1]-font_size[1]/2), font_size), 2)
        self.screen.blit(self.text_surf, self.text_box)

    def update(self, dialog):
        self.dialog = dialog
        self.draw()

    def in_boundaries(self, position):
        return self.text_box.collidepoint(position)

    def text_objects(self, text, font):
        text_surface = font.render(text, 1, self.TEXT_COLOR)
        return text_surface, text_surface.get_rect()