from window import Window
from pygame import KEYDOWN, MOUSEBUTTONDOWN, K_SPACE, K_1, K_2, K_s, K_a
from pygame.mouse import get_pressed as pyg_get_pressed
from pygame.mouse import get_pos as pyg_get_pos
from threading import Thread
from algorithms import BreadthFirstSearch, DijkstraUniformCostSearch, AStarPathing
from snake import Snake, RunSnakeAI
from cells import Contents
from numpy import ndindex as np_iter
from config import settings


class AlgorithmHandler(Window):

    def __init__(self):
        super().__init__()

        self.can_clear = False  # clear the board of scanned tiles

        self.draw_type = Contents.WALL
        #  Initialising Algorithms
        self.breadth = BreadthFirstSearch(
            self.grid,
            *self.grid.fixed_cells # [start, end]
        )
        self.dijkstra = DijkstraUniformCostSearch(
            self.grid,
            *self.grid.fixed_cells # [start, end]
        )
        self.astar = AStarPathing(
            self.grid,
            *self.grid.fixed_cells # [start, end]
        )
        snake_head_x, snake_head_y = self.grid.fixed_cells[0].x, self.grid.fixed_cells[0].y
        snake = Snake(self.grid, (snake_head_x, snake_head_y))
        self.jabsnake = RunSnakeAI(snake, self.grid)

    def handle_events(self, event):
        super().handle_events(event)
        mouse_pos = pyg_get_pos()

        if event.type == KEYDOWN:
            if not settings.running_algorithm:
                if event.key == K_SPACE:
                    settings.running_algorithm = True
                    self.grid.empty_path()
                    self.breadth.reset(self.grid, *self.grid.fixed_cells)
                    algorithm = Thread(target=self.breadth.run, daemon=True)
                    algorithm.start()
                    self.can_clear = True
                elif event.key == K_s:
                    algorithm = Thread(target=self.jabsnake.run, daemon=True)
                    algorithm.start()
                elif event.key == K_a:
                    settings.running_algorithm = True
                    self.grid.empty_path()
                    self.astar.reset(self.grid, *self.grid.fixed_cells)
                    algorithm = Thread(target=self.astar.run, daemon=True)
                    algorithm.start()
                    self.can_clear = True
            elif event.key == K_1:
                self.draw_type = Contents.WALL
            elif event.key == K_2:
                self.draw_type = Contents.FIELD

        elif not settings.running_algorithm:
            if pyg_get_pressed(5)[0]: # user drawing cells
                for x, y in np_iter(self.grid.shape): # iterating using np (gaming)
                    if self.grid.get_cell(x, y).rect.collidepoint(mouse_pos):
                        self.grid.set_cell(x, y, self.draw_type)

            elif pyg_get_pressed(5)[2]: # user erasing cells
                for x, y in np_iter(self.grid.shape):
                    if self.grid.get_cell(x, y).rect.collidepoint(mouse_pos):
                        self.grid.set_cell(x, y, Contents.EMPTY)

            # on new draw clear previous paths and scans
            if self.can_clear and event.type == MOUSEBUTTONDOWN:
                self.can_clear = False
                self.grid.empty_path()



