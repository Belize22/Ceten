from abc import ABC, abstractmethod


class Button(ABC):
    def __init__(self, screen, position):
        self.screen = screen
        self.position = position
        self.enabled = False
        super().__init__()

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def in_boundaries(self, position):
        pass

    def switch_enabled_state(self):
        self.enabled = not self.enabled
        self.draw()




