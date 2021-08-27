from config import Widgets, settings

class Button:
    def __init__(self, image):
        # converting surface to improve performance
        self.img = image.convert()
        self.rect = self.img.get_rect()

    def draw(self, screen, x, y):
        screen.blit(self.img, (x, y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def run(self):
        raise NotImplementedError("unpog")


class ResetButton(Button):
    def __init__(self, grid):
        super().__init__(Widgets.reset_button)
        self.grid = grid

    def run(self):
        settings.running_algorithm = False
        self.grid.empty_grid()
        self.grid.gen_fixed_cells()


class ButtonManager:
    def __init__(self, grid):
        self.grid = grid
        self.buttons = []
        self.reset_button = ResetButton(grid)

    def add_button(self, button: Button):
        self.buttons.append(button)

    def get_clicked(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                return button

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()
