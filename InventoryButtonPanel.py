from Panel import Panel
from InventoryButton import InventoryButton


class InventoryButtonPanel(Panel):
    SHIFT_FACTOR = 35

    def __init__(self, screen, position, button_quantity, orientation):
        super().__init__(screen, position)
        self.buttons = []
        x_offset = 10
        for i in range(0, button_quantity):
            new_button = InventoryButton(
                self.screen, [int(self.center[0] + x_offset),
                              int(self.center[1])],
                orientation)
            self.buttons.append(new_button)
            x_offset += self.SHIFT_FACTOR

    def draw(self):
        for i in range(0, len(self.buttons)):
            self.buttons[i].draw()

    def toggle_button_in_boundary(self, position):
        for i in range(0, len(self.buttons)):
            if (self.buttons[i].in_boundaries(position)
               and self.buttons[i].enabled):
                return i
        return -1
