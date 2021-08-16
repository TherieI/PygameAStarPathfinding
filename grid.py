import cells, config
import pygame
from random import randint
import numpy as np

# Tiles in an array
class Grid:
    def __init__(self, window):
        # generating empty grid
        self.grid = np.full(config.grid_dimensions.xy, cells.Cell)
        self.init_grid()
        self.shape = self.grid.shape
        self.window = window
        # generating fixed cells (start, end)
        self.fixed_cells = []
        self.gen_fixed_cells()

    def init_grid(self): # setting all cells to empty and creating the rects
        rect_width, rect_height = (
            int(config.window_resolution.x/config.grid_dimensions.x),
            int((config.window_resolution.y - config.settings.grid_buffer)/config.grid_dimensions.y)
        )

        for x, y in np.ndindex(self.grid.shape):
            # pygame.rect.Rect((position), (width/length))
            rect = pygame.rect.Rect(
                (x*rect_width, y*rect_height + config.settings.grid_buffer),
                (rect_width, rect_height)
            )
            self.grid[x, y] = cells.Cell(x, y, cells.Contents.EMPTY, rect)

    def empty_grid(self):
        for x, y in np.ndindex(self.grid.shape):
            self.grid[x, y].cont = cells.Contents.EMPTY

    def empty_path(self):
        for x, y in np.ndindex(self.grid.shape):
            if self.grid[x, y].is_path():
                self.grid[x, y].cont = cells.Contents.EMPTY

    def gen_fixed_cells(self):
        self.fixed_cells = []
        fixed_cells_cont = (cells.Contents.START, cells.Contents.END)
        for fixed_cell_cont in fixed_cells_cont:
            rand_x, rand_y = (
                randint(0, config.grid_dimensions.x - 1),
                randint(0, config.grid_dimensions.y - 1)
            )
            self.grid[rand_x, rand_y].cont = fixed_cell_cont
            self.fixed_cells.append(self.grid[rand_x, rand_y])

    # returns a random cell, can exclude certain cell types
    def rand_cell(self, exclude=()):
        cell = None
        while cell is None or cell.cont in exclude:
            cell = self.get_cell(
                randint(0, config.grid_dimensions.x - 1),
                randint(0, config.grid_dimensions.y - 1)
            )
        return cell

    def set_cell(self, x, y, cont, override=False):
        if not self.grid[x, y].is_fixed() or override:
            self.grid[x, y].cont = cont

    def get_cell(self, x, y):
        if 0 <= x < config.grid_dimensions.x and 0 <= y < config.grid_dimensions.y:
            return self.grid[x, y]
        return None

    @staticmethod
    def dist_between(start: cells.Cell, end: cells.Cell):
        return ((start.x - end.x)**2 + (start.y - end.y)**2)**0.5
