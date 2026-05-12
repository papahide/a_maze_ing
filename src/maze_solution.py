from src.maze_generation import MazeGenerator, NORTH, EAST, WEST, SOUTH
from collections import deque


class MazeSolution:
    def __init__(self, maze_gen: MazeGenerator,
                 entry: tuple[int, int],
                 exit_point: tuple[int, int]) -> None:
        self.maze: list[list[int]] = maze_gen.maze
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_point
        self.explored: list[tuple[int, int]] = []
        self.path: list[tuple[int, int]] = []
        self.directions: str = ""

    def get_neighbours(
                       self,
                       curr_cell: tuple[int, int]
                       ) -> list[tuple[int, int]]:
        x, y = curr_cell
        neighbours: list[tuple[int, int]] = []
        if not self.maze[y][x] & NORTH:
            neighbours.append((x, y-1))
        if not self.maze[y][x] & EAST:
            neighbours.append((x+1, y))
        if not self.maze[y][x] & WEST:
            neighbours.append((x-1, y))
        if not self.maze[y][x] & SOUTH:
            neighbours.append((x, y+1))
        return neighbours

    @staticmethod
    def get_direction(son: tuple[int, int], father: tuple[int, int]) -> str:
        sx, sy = son
        fx, fy = father
        if sx > fx:
            return "E"
        elif sx < fx:
            return "W"
        elif sy < fy:
            return "N"
        else:
            return "S"

    def solve(self) -> None:
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        queue.append(self.entry)
        visited.add(self.entry)
        while queue:
            self.explored.append(queue.popleft())
            curr_cell = self.explored[-1]
            if curr_cell == self.exit:
                cell: tuple[int, int] = self.exit
                while cell != self.entry:
                    self.path.append(cell)
                    self.directions += self.get_direction(cell,
                                                          came_from[cell])
                    cell = came_from[cell]
                self.path.append(self.entry)
                self.path.reverse()
                break
            directions: list[tuple[int, int]] = self.get_neighbours(curr_cell)
            for direction in directions:
                if direction not in visited:
                    visited.add(direction)
                    came_from[direction] = curr_cell
                    queue.append(direction)
