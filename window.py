# refactored game class
import button
import cells
import config
import grid
import interface
import numpy as np
import pygame
import sys


# displays grid
class Window:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(config.window_resolution.with_buffer())
        pygame.display.set_caption("Pathfinding")

        self.clock = pygame.time.Clock()
        self.grid = grid.Grid()
        self.running_algorithm = False

        self.button_manager = button.ButtonManager(self.grid)

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
        interface.fill_background(self.screen)
        interface.draw_border(self.screen, (config.window_resolution.left, config.window_resolution.top), config.window_resolution.xy, cells.Palette.DARKGREY, cells.Palette.LIGHTGREY) # border around grid
        interface.draw_border(self.screen, (int(config.window_resolution.x/2)-10, config.window_resolution.top-70), (60, 60), cells.Palette.DARKGREY, cells.Palette.LIGHTGREY)  # border around settings

        # drawing grid
        self.grid.draw(self.screen)

        self.button_manager.draw_buttons()

    def handle_button_events(self, event):
        pass
