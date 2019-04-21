import pygame


class NotificationPanel:
    def __init__(self, position, screen):
        self.dialog = ""
        self.center = position
        self.screen = screen

    def update(self, dialog):
        self.dialog = dialog

    def draw(self):
        pygame.draw.rect(self.screen, (205, 228, 205),
                         ((self.screen.get_width()*0.2, self.center[1]),
                          (self.screen.get_width()*0.6,
                           self.screen.get_height()*0.05)))
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.dialog), 1, (10, 10, 10))
        font_width, font_height = font.size(str(self.dialog))
        self.screen.blit(text, (self.center[0]-font_width*0.5, self.center[1]))
