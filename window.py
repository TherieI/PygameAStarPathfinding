# refactored game class
import cells, config, grid
import pygame
import sys
import numpy as np

# displays grid
class Window:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(config.window_resolution.xy)
        self.clock = pygame.time.Clock()
        self.grid = grid.Grid(self)
        self.running_algorithm = False

        pygame.display.set_caption("dipaly")

    def run(self):
        while True:
            self.clock.tick(120)
            for event in pygame.event.get():
                self.handle_events(event)
            self.draw()
            pygame.display.update()

    def handle_events(self, event):
        if event.type == pygame.QUIT: # you guessed it
            pygame.quit()
            sys.exit()

    def draw(self):
        # background
        self.screen.fill(cells.Palette.LIGHTGREY)

        # drawing nodes
        for x, y in np.ndindex(self.grid.shape):
            cell = self.grid.get_cell(x, y)
            pygame.draw.rect(
                self.screen,
                cells.Palette.get_color(cell.cont),
                cell.rect,
                width = 1 if cell.cont == cells.Contents.EMPTY else 0 # border drawing stuff
            )
        self.draw_buttons()

    def draw_buttons(self):
        self.screen.blit(config.widgets.reset_button, (3, 3))

