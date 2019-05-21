import pygame


class InventoryPanel:
    SHIFT_FACTOR = 17.5

    def __init__(self, position, screen, quantities, icons, icon_size):
        self.center = position
        self.screen = screen
        self.quantities = quantities
        self.icons = icons
        self.icon_size = icon_size

    def update(self, quantities):
        self.quantities = quantities

    def draw(self):
        x_offset = 0
        for i in range(0, len(self.quantities)):
            icon_rect = pygame.draw.rect(
                self.screen, (0, 0, 0),
                ((self.center[0] + x_offset, self.center[1]),
                 (self.icon_size[0], self.icon_size[1])), 0)
            icon_image = pygame.image.load(self.icons[i])
            icon_texture = pygame.transform.scale(
                icon_image, icon_rect.size)
            self.screen.blit(icon_texture, icon_rect)
            x_offset += self.SHIFT_FACTOR
            self.__render_blit(
                str(self.quantities[i]),
                (self.center[0] + x_offset, self.center[1]))
            x_offset += self.SHIFT_FACTOR

    def __render_blit(self, string, point):
        font = pygame.font.Font(None, 24)
        text = font.render(string, 1, (10, 10, 10))
        self.screen.blit(text, point)
