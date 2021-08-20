from config import Widgets, settings
from pygame.Rect import collidepoint as has_collided

class ButtonManager:
    def __init__(self, grid):
        self.grid = grid

        self.reset_button = ResetButton(grid)

class Button:
    _list = []
    def __init__(self, image):
        # converting surface to improve performance
        self.img = image.convert()
        self.rect = self.image.get_rect()
        Button._list.append(self)

    def draw(self, screen, x, y):
        screen.blit(self.img, (x, y))

    def is_clicked(self, mouse_pos):
        return self.rect.has_collided(mouse_pos)

    def run(self):
        raise NotImplementedError("unpog")

    @staticmethod
    def get_buttons():
        return Button._list


class ResetButton(Button):
    def __init__(self, grid):
        super().__init__(Widgets.reset_button)
        self.grid = grid

    def run(self):
        settings.running_algorithm = False
        self.grid.empty_grid()
        self.grid.gen_fixed_cells()
