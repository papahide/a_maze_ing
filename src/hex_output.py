from src.maze_generation import MazeGenerator, NORTH, EAST, WEST, SOUTH
from src.parser import MazeConfig

class HexOutput:
    """
    Class that contains the methods that converts
    the maze cells to hex.
    And writes in a output file the maze in hexadecimal,
    the entry, exit and the solution
    """
    def __init__(self, maze_gen: MazeGenerator,
                 entry: tuple[int, int],
                 exit_point: tuple[int, int],
                 solution: str,
                 conf: MazeConfig) -> None:
        """
        Main constructor of the class.
        Defines all attributes of the class.
        It uses data from MazeConfig and MazeGenerator
        """
        self.maze: list[list[int]] = maze_gen.maze
        self.width: int = conf.width
        self.height: int = conf.height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_point
        self.solution: str = solution
        self.output_file: str = conf.output_file

    def hex_cell(self, cell_pos: tuple[int, int]) -> str:
        """
        This method converts a cell from binary to hexadecimal
        """
        x, y = cell_pos
        value: int = 0
        if self.maze[y][x] & NORTH:
            value += 1
        if self.maze[y][x] & EAST:
            value += 2
        if self.maze[y][x] & SOUTH:
            value += 4
        if self.maze[y][x] & WEST:
            value += 8
        return format(value, "X")

    def hex_maze(self) -> str:
        """
        Cretes all the maze lines, to be
        written in the output file.
        """
        output: str = ""
        for y in range(self.height):
            line: str = ""
            for x in range(self.width):
                line += self.hex_cell((x, y))
            output += line + "\n"
        return output

    def hex_output(self) -> None:
        """
        This is the main method that writes all
        the data in the output file.
        """
        with open(self.output_file, "w") as file:
            maze_txt: str = self.hex_maze()
            file.write(maze_txt)
            file.write("\n")
            entry_txt: str = f"{self.entry[0],self.entry[1]}"
            file.write((entry_txt) + "\n")
            exit_txt: str = f"{self.exit[0],self.exit[1]}"
            file.write((exit_txt) + "\n")
            solution_txt: str = self.solution
            file.write((solution_txt) + "\n")
