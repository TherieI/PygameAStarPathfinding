from cells import Palette
from pygame import Surface

def fill_background(screen):
    screen.fill(Palette.LIGHTGREY)

def draw_border(screen, position, dimensions, border_color, inside_color, border_width=10):  # draws a border of with external width
    background = Surface([dim+2*border_width for dim in dimensions])
    background.fill(border_color)

    foreground = Surface(dimensions)
    foreground.fill(inside_color)

    Surface.blit(background, foreground, (border_width, border_width))
    Surface.blit(screen, background, [pos-10 for pos in position])
