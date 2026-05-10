from src.parser import MazeConfig
import random


NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


class MazeGenerator():
    def __init__(self, conf: MazeConfig) -> None:
        self.width: int = conf.width
        self.height: int = conf.height
        self.seed: int = conf.seed
        self.perfect: bool = conf.perfect
        self.entry: tuple[int, int] = conf.entry_point
        self.exit: tuple[int, int] = conf.exit_point
        self.maze: list[list[int]] = self.maze_init()
        self.visited: list[list[bool]] = [[False for _ in range(conf.width)]
                                          for _ in range(conf.height)]
        self.solution: list[tuple[int, int]] = []

    def maze_init(self) -> list[list[int]]:
        return [[0b1111 for _ in range(self.width)]
                for _ in range(self.height)]

    def mark_visited_cell(self, curr_cell: tuple[int, int]) -> None:
        x, y = curr_cell
        self.visited[y][x] = True

    def get_not_visited(self, curr_cell:
                        tuple[int, int]) -> list[tuple[int, int]]:
        not_visited: list[tuple[int, int]] = []
        x, y = curr_cell
        if x > 0 and not self.visited[y][x-1]:
            not_visited.append((x-1, y))
        if x < self.width - 1 and not self.visited[y][x+1]:
            not_visited.append((x+1, y))
        if y > 0 and not self.visited[y-1][x]:
            not_visited.append((x, y-1))
        if y < self.height - 1 and not self.visited[y+1][x]:
            not_visited.append((x, y+1))
        return not_visited

    def remove_walls(self, curr_cell: tuple[int, int],
                     new_cell: tuple[int, int]) -> None:
        x, y = curr_cell
        nx, ny = new_cell
        if x > nx:
            self.maze[y][x] &= ~WEST
            self.maze[ny][nx] &= ~EAST
        if x < nx:
            self.maze[y][x] &= ~EAST
            self.maze[ny][nx] &= ~WEST
        if y < ny:
            self.maze[y][x] &= ~SOUTH
            self.maze[ny][nx] &= ~NORTH
        if y > ny:
            self.maze[y][x] &= ~NORTH
            self.maze[ny][nx] &= ~SOUTH

    def dfs_backtracking(self, start: tuple[int, int]) -> None:
        stack: list[tuple[int, int]] = []
        stack.append(start)
        while stack:
            curr_cell: tuple[int, int] = stack[-1]
            not_visited: list[tuple[int,
                                    int]] = self.get_not_visited(curr_cell)
            if not_visited:
                random.shuffle(not_visited)
                new_cell: tuple[int, int] = not_visited[0]
                self.remove_walls(curr_cell, new_cell)
                self.mark_visited_cell(new_cell)
                stack.append(new_cell)
            else:
                stack.pop(-1)

    def get_walls(self) -> list[list[tuple[int, int]]]:
        walls: list[list[tuple[int, int]]] = []
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1 and self.maze[y][x] & EAST:
                    walls.append([(x, y), (x+1, y)])
                if y < self.height - 1 and self.maze[y][x] & SOUTH:
                    walls.append([(x, y), (x, y+1)])
        return walls

    def check_empty_zone(self) -> bool:
        
        return False

    def remove_wall(self, to_remove: list[tuple[int, int]]) -> None:
        pass

    def make_maze_imperfect(self) -> None:
        walls: list[list[tuple[int, int]]] = self.get_walls()
        n_walls_to_remove: int = int(len(walls) * 0.15)
        random.shuffle(walls)
        for _ in range(n_walls_to_remove):
            to_remove: list[tuple[int, int]] = walls[0]
            if self.check_empty_zone():
                self.remove_wall(to_remove)
                walls.pop(0)
            walls.pop(0)

    def fill_cell(self, x: int, y: int) -> None:
        directions: list[int] = [NORTH, EAST, SOUTH, WEST]
        for direction in directions:
            self.maze[y][x] |= direction
            if direction == NORTH and y > 0:
                self.maze[y-1][x] |= SOUTH
            if direction == EAST and x < self.width - 1:
                self.maze[y][x+1] |= WEST
            if direction == SOUTH and y < self.height - 1:
                self.maze[y+1][x] |= NORTH
            if direction == WEST and x > 0:
                self.maze[y][x-1] |= EAST

    def put_center_pattern(self) -> None:
        """
        Create the 42 center pattern
        """
        center: tuple[int, int] = (self.width // 2, self.height // 2)
        x, y = center
        cells: list[tuple[int, int]] = [
            (x-3, y-2),
            (x-3, y-1),
            (x-3, y),
            (x-2, y),
            (x-1, y),
            (x-1, y+1),
            (x-1, y+2),
            (x+1, y-2),
            (x+2, y-2),
            (x+3, y-2),
            (x+3, y-1),
            (x+3, y),
            (x+2, y),
            (x+1, y),
            (x+1, y+1),
            (x+1, y+2),
            (x+2, y+2),
            (x+3, y+2),
        ]
        for x, y in cells:
            self.fill_cell(x, y)

    def maze_gen(self) -> None:
        random.seed(self.seed)
        start: tuple[int, int] = self.entry
        self.mark_visited_cell(start)
        self.dfs_backtracking(start)
        if not self.perfect:
            self.make_maze_imperfect()
        if self.width > 12 and self.height > 10:
            self.put_center_pattern()
