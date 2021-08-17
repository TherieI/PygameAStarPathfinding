from cells import Contents
from grid import Grid
from queue import Queue, PriorityQueue
from time import sleep
import config

class PriorityQueueRefactored(PriorityQueue):  # for dijkstras
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


class PatherTemplate:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end

        self.algorithm_speed = 0

    def set_speed(self, speed):
        self.algorithm_speed = speed

    def neighbors(self, cell, cardinal_only=True):
        all_neighbors = list(filter(None.__ne__, [  # filters out all neighbors that are out of map bounds
            self.grid.get_cell(cell.x, cell.y + 1),
            self.grid.get_cell(cell.x - 1, cell.y),
            self.grid.get_cell(cell.x, cell.y - 1),
            self.grid.get_cell(cell.x + 1, cell.y)
        ]))
        if not cardinal_only:
            all_neighbors += list(filter(None.__ne__, [  # filters out all neighbors that are out of map bounds
                self.grid.get_cell(cell.x - 1, cell.y + 1),
                self.grid.get_cell(cell.x + 1, cell.y + 1),
                self.grid.get_cell(cell.x - 1, cell.y - 1),
                self.grid.get_cell(cell.x + 1, cell.y - 1)
            ]))
        final_neighbors = []
        for n in all_neighbors:
            if n.cont not in (Contents.WALL, Contents.SNAKE):
                final_neighbors.append(n)
        return final_neighbors

    def get_best_path(self, all_paths):
        current = self.end
        path = []
        while current != self.start:
            path.append(current)
            current = all_paths[current]
        path.reverse()
        return path

    def draw_path(self, path):
        for cell in path:
            if not cell.is_fixed():
                cell.cont = Contents.PATH

    def run(self):
        """Plot the route, Draw to screen"""
        raise NotImplementedError("Inherit PatherTemplate for your own pather sussy baka :weary:")

    def reset(self, grid, start, end, new_nodes=False):
        self.__init__(grid, start, end)
        if new_nodes:
            grid.gen_fixed_cells()


class BreadthFirstSearch(PatherTemplate):
    def __init__(self, grid, start, end):
        super().__init__(grid, start, end)

        self.frontier = Queue()
        self.frontier.put(start)

        self.came_from = dict()
        self.came_from[start] = None

    def get_all_paths(self, visual_scan=True):
        found = False
        while not self.frontier.empty():
            sleep(self.algorithm_speed)
            current = self.frontier.get()
            if current == self.end:
                found = True
                break
            for cell in self.neighbors(current, cardinal_only=config.settings.neighbor_type):
                if visual_scan and not cell.is_fixed():
                    cell.cont = Contents.SCANNED
                if cell not in self.came_from:
                    self.frontier.put(cell)
                    self.came_from[cell] = current
        if not found:
            return None
        return self.came_from

    def run(self):
        paths = self.get_all_paths()
        if paths is None:
            print("Path Not Found")
            return
        path = self.get_best_path(paths)
        self.draw_path(path)


class DijkstraUniformCostSearch(PatherTemplate):
    def __init__(self, grid, start, end):
        super().__init__(grid, start, end)
        self.frontier = PriorityQueueRefactored()
        self.frontier.put(start, 0)
        self.came_from = dict()
        self.cost_so_far = dict()
        self.came_from[start] = None
        self.cost_so_far[start] = 0

    def run(self):
        found = False
        while not self.frontier.empty():
            current = self.frontier.get()
            if current == self.end:
                found = True
                break
            for cell in self.neighbors(current):
                new_cost = self.cost_so_far[current] + self.cost(cell)
                if not cell.is_fixed() and not cell.is_field():
                    cell.cont = Contents.SCANNED
                if cell not in self.cost_so_far or new_cost < self.cost_so_far[cell]:
                    self.cost_so_far[cell] = new_cost
                    priority = new_cost
                    self.frontier.put(cell, priority)
                    self.came_from[cell] = current
        if not found:
            print("Path not found")
            return
        current = self.end
        path = []
        while current != self.start:
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        for cell in path:
            if not cell.is_fixed():
                cell.cont = Contents.PATH

    def cost(self, cell):
        if cell.cont == Contents.FIELD:
            return 1.5
        return 1

class AStarPathing(PatherTemplate):

    def __init__(self, grid, start, end):
        super().__init__(grid, start, end)

        self.directions = dict()
        self.directions[self.start] = None

        self.open = set()
        self.closed = set()
        start.cost = self.h_cost(end)
        self.open.add(start)

    def get_all_paths(self):  # inspired by sebastian lague https://www.youtube.com/watch?v=-L-WgKMFuhE
        found = False
        while not found:
            current = self.get_best_cell()
            self.open.remove(current)
            self.closed.add(current)

            sleep(self.algorithm_speed)
            if current == self.end:
                found = True
                break

            for neighbor_cell in self.neighbors(current, cardinal_only=True):
                if neighbor_cell not in self.closed:
                    if not neighbor_cell.is_fixed() and not neighbor_cell.is_field():
                        neighbor_cell.cont = Contents.SCANNED
                    if neighbor_cell.cost < current.cost or neighbor_cell not in self.open:
                        neighbor_cell.cost = self.g_cost(neighbor_cell) + self.h_cost(neighbor_cell)
                        self.directions[neighbor_cell] = current
                        if neighbor_cell not in self.open:
                            self.open.add(neighbor_cell)
        return found

    def run(self):
        found = self.get_all_paths()
        if not found:
            print("Path Not Found")
            return
        path = self.get_best_path(self.directions)
        self.draw_path(path)

    def g_cost(self, cell):
        return Grid.dist_between(self.start, cell)

    def h_cost(self, cell):
        return Grid.dist_between(self.end, cell)

    def get_best_cell(self):  # returns the cell with minimum cost and updates all costs in open
        def first_element(_set: set):  # stupid but fastest way I could find online
            for first in _set:
                return first

        min_cell = first_element(self.open)
        min_cell_val = min_cell.cost
        for cell in self.open:
            f_cost = self.g_cost(cell) + self.h_cost(cell)
            cell.cost = f_cost
            if f_cost < min_cell_val:
                min_cell = cell
                min_cell_val = f_cost
        return min_cell


