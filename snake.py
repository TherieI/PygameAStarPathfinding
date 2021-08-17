from config import grid_dimensions
from cells import Contents
from algorithms import BreadthFirstSearch
from random import randint
from time import sleep


class Snake:

    UP = 0, 1
    DOWN = 0, -1
    LEFT = -1, 0
    RIGHT = 1, 0

    def __init__(self, grid, start_position):
        self.grid = grid
        self.head = start_position
        self.body = [self.head]
        self.direction = Snake.UP

        self.path = []

    def draw(self):
        for body_pos_x, body_pos_y in self.body:
            self.grid.set_cell(body_pos_x, body_pos_y, Contents.SNAKE)

    def move(self):
        head_x, head_y = self.head
        velocity_x, velocity_y = self.direction

        self.head = (head_x + velocity_x, head_y - velocity_y) # new head
        self.body.insert(0, self.head)  # inserting new head at start
        self.grid.set_cell(*self.body[-1], Contents.EMPTY)
        del self.body[-1]  # deleting tail

    def follow_path(self):
        next_move = self.path[0]
        head_x, head_y = self.head
        if head_x + 1 == next_move.x:
            self.set_direction(Snake.RIGHT)
        elif head_x - 1 == next_move.x:
            self.set_direction(Snake.LEFT)
        elif head_y - 1 == next_move.y:
            self.set_direction(Snake.UP)
        elif head_y + 1 == next_move.y:
            self.set_direction(Snake.DOWN)
        del self.path[0]

    def set_path(self, new_path):
        self.path = new_path

    def set_direction(self, direction):
        if self.direction != [i*-1 for i in direction]:  # checks to see if the new direction is not opposite the old direction (troll)
            self.direction = direction

    def has_died(self):
        # testing for if player collided with themselves by finding a duplicate coord in list
        if len(self.body) != len(set(self.body)):
            return True
        # testing if player out of bounds
        elif not (grid_dimensions.x > self.body[0][0] >= 0) or not (grid_dimensions.y > self.body[0][1] >= 0):
            return True
        return False

    def increase_size(self):
        self.body.append((-1, -1))  # gaming code


class Food:
    def __init__(self, grid):
        self.grid = grid
        self.x, self.y = self.grid.fixed_cells[1].x, self.grid.fixed_cells[1].y

    def new_position(self):
        self.grid.set_cell(self.x, self.y, Contents.EMPTY, override=True)
        cell = self.grid.rand_cell(exclude=(Contents.SNAKE, Contents.WALL))
        self.x, self.y = cell.x, cell.y

    def draw(self):
        self.grid.set_cell(self.x, self.y, Contents.END)


class RunSnakeAI:
    def __init__(self, snake, grid):
        self.snake = snake
        self.food = Food(grid)
        self.grid = grid
        self.pathfinder = None

    def get_path(self):
        paths = self.pathfinder.get_all_paths(visual_scan=False)
        return self.pathfinder.get_best_path(paths)

    def run(self):

        self.grid.set_cell(*self.snake.head, Contents.EMPTY, override=True)
        start_cell, end_cell = self.grid.get_cell(*self.snake.head), self.grid.get_cell(self.food.x, self.food.y)
        self.pathfinder = BreadthFirstSearch(self.grid, start_cell, end_cell)
        path = self.get_path()
        self.snake.set_path(path)

        while not self.snake.has_died():
            if self.snake.path == []:  # hit the food when path ran out
                # generating new food and increasing snake size
                self.food.new_position()
                self.snake.increase_size()
                self.food.draw()

                # pathfinding new food location
                start_cell, end_cell = self.grid.get_cell(*self.snake.head), self.grid.get_cell(self.food.x, self.food.y)
                self.pathfinder.reset(self.grid, start_cell, end_cell)
                try:
                    path = self.get_path()
                except TypeError:
                    print("snaek unable to locate food")
                self.snake.set_path(path)

            # drawing snake
            self.snake.follow_path()
            self.snake.move()
            self.snake.draw()
            sleep(0.001)


