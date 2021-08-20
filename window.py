# refactored game class
import cells, config, grid
import pygame
import sys
import numpy as np
import button

# displays grid
class Window:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(config.window_resolution.xy)
        pygame.display.set_caption("Pathfinding")

        self.clock = pygame.time.Clock()
        self.grid = grid.Grid(self)
        self.running_algorithm = False


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
        self.handle_button_events(event)

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

    def handle_button_events(self, event):
        pass
