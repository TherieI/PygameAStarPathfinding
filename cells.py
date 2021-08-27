from dataclasses import dataclass, field
from enum import Enum
from pygame.rect import Rect

class Contents(Enum):
    START = 1
    END = 2
    WALL = 3
    EMPTY = 4
    SCANNED = 5
    PATH = 6
    FIELD = 7
    SNAKE = 8

class Palette:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    LIGHTGREY = (230, 230, 230)
    DARKGREY = (100, 100, 100)
    WHITE = (255, 255, 255)
    LIGHTBLUE = (0, 200, 220)
    BLUE = (0, 0, 255)
    DARKGREEN = (0, 100, 0)
    SNAKE_GREEN = (81, 209, 67)

    @staticmethod
    def get_color(cont: Contents):
        if cont == Contents.START:
            return Palette.GREEN
        elif cont == Contents.END:
            return Palette.RED
        elif cont == Contents.WALL:
            return Palette.DARKGREY
        elif cont == Contents.EMPTY:
            return Palette.WHITE
        elif cont == Contents.SCANNED:
            return Palette.LIGHTBLUE
        elif cont == Contents.PATH:
            return Palette.BLUE
        elif cont == Contents.FIELD:
            return Palette.DARKGREEN
        elif cont == Contents.SNAKE:
            return Palette.SNAKE_GREEN

@dataclass(unsafe_hash=True)
class Cell:
    x: int
    y: int
    cont: Contents = field(compare=False)
    rect: Rect = field(repr=False, compare=False)
    cost: int = field(default=0, compare=False)

    def is_fixed(self):
        return self.cont in (Contents.START, Contents.END)

    def is_field(self):
        return self.cont == Contents.FIELD

    def is_path(self):
        return self.cont in (Contents.PATH, Contents.SCANNED, Contents.FIELD)

