from abc import ABC, abstractmethod


class Panel(ABC):
    def __init__(self, screen, position):
        self.screen = screen
        self.center = position
        super().__init__()

    @abstractmethod
    def draw(self):
        pass
