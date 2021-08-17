from dataclasses import dataclass
from pygame.image import load

class Dimensions:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = x, y

@dataclass
class Settings:
    grid_buffer: int
    neighbor_type: bool # true: 8 diagonal adjacent / false: 4 adjacent per cell
    field_cell_weight: float
    algorithm_speed: float


class Widgets:
    reset_button = load("resources/reset_button.jpg")


# Window Resolution
WINDOW_RESOLUTION_X = 800
WINDOW_RESOLUTION_Y = 800
GRID_BUFFER = 50  # represents the size of the bar at the top where you can change settings

GRID_DIMENSION_X = 40
GRID_DIMENSION_Y = 40

window_resolution = Dimensions(WINDOW_RESOLUTION_X, WINDOW_RESOLUTION_Y + GRID_BUFFER)
grid_dimensions = Dimensions(GRID_DIMENSION_X, GRID_DIMENSION_Y)

widgets = Widgets()
settings = Settings(GRID_BUFFER, False, 1.5)
