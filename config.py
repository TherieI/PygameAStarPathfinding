from dataclasses import dataclass
from pygame.image import load

class Dimensions:
    def __init__(self, x, y, top_buffer=0, bottom_buffer=0, left_buffer=0, right_buffer=0):
        self.x = x
        self.y = y
        self.xy = x, y

        # Buffers
        self.top = top_buffer
        self.bottom = bottom_buffer
        self.left = left_buffer
        self.right = right_buffer

    def with_buffer(self):
        return self.x + self.left + self.right, self.y + self.top + self.bottom

@dataclass
class Settings:
    neighbor_type: bool # true: 4 diagonal adjacent / false: 8 adjacent per cell
    field_cell_weight: float
    algorithm_speed: float
    running_algorithm: bool = False


class Widgets:
    reset_button = load("resources/reset_button.jpg")


# Window Resolution
WINDOW_RESOLUTION_X = 800
WINDOW_RESOLUTION_Y = 800

# Buffers
GRID_BUFFER_TOP = 80  # represents the size of the bar at the top where you can change settings
GRID_BUFFER_BOTTOM = 20
GRID_BUFFER_LEFT = 20
GRID_BUFFER_RIGHT = 20


# Number of rows and columns
GRID_DIMENSION_X = 40
GRID_DIMENSION_Y = 40

window_resolution = Dimensions(WINDOW_RESOLUTION_X, WINDOW_RESOLUTION_Y, top_buffer=GRID_BUFFER_TOP, bottom_buffer=GRID_BUFFER_BOTTOM, left_buffer=GRID_BUFFER_LEFT, right_buffer=GRID_BUFFER_RIGHT)
grid_dimensions = Dimensions(GRID_DIMENSION_X, GRID_DIMENSION_Y)

settings = Settings(True, 1.5, 0.01)
