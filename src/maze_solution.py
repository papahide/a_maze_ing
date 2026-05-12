from src.maze_generation import MazeGenerator, NORTH, EAST, WEST, SOUTH
from collections import deque


class MazeSolution:
    """
    Class containing the maze solution methods.
    It uses the DFS algorithm
    """
    def __init__(self, maze_gen: MazeGenerator,
                 entry: tuple[int, int],
                 exit_point: tuple[int, int]) -> None:
        """
        Declaration of the magic method of the MazeSolution
        class defines the attributes
        """
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
        """
        This method searches the adjacent cells
        (that can be accessed) and returns them in a list
        """
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
        """
        This static method returns the direction in witch the solution
        path is moving in that specific cell
        """
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
        """
        Main method to create the solution of the maze with the DFS algorithm:
          - Create a queue using deque (uses queue.popleft,
            faster than regular pop)
          - Creates auxiliar variables, to store data
            like: came_from[son] = father,
            visited (visited cells)
          - While the wue has data, it explores every possible path
            in the maze.
          - Stores the shorthest path between entry and exit points.
        """
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
