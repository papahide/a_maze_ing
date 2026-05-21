from .maze_generation import MazeGenerator, MazeConfig, NORTH, WEST
from .maze_solution import MazeSolution
from PIL import Image, ImageDraw


class MazeRender():
    def __init__(self, the_maze: MazeGenerator,
                 conf: MazeConfig,
                 sol: MazeSolution,
                 maze_theme: dict[str, str] | None = None,
                 sol_hide: bool = True
                 ) -> None:
        self.maze: list[list[int]] = the_maze.maze
        self.height: int = conf.height
        self.width: int = conf.width
        self.entry: tuple[int, int] = conf.entry_point
        self.exit: tuple[int, int] = conf.exit_point
        self.solution: set[tuple[int, int]] = set(sol.path)
        self.forty_two: set[tuple[int, int]] | None = set(the_maze.fortytwo) if the_maze.fortytwo else None
        self.maze_str: str = ""
        self.hide_solution: bool = sol_hide
        if maze_theme:
            self.theme: dict[str, str] = maze_theme
        else:
            self.theme: dict[str, str] = {"wall": "██",
                                          "path": "\033[32m██\033[0m",
                                          "entry": "\033[33m██\033[0m",
                                          "exit": "\033[31m██\033[0m",
                                          "fortytwo": "\033[34m██\033[0m"}

    def cell_content(self, cell: tuple[int, int]) -> str:
        if cell == self.entry:
            return self.theme["entry"]
        elif cell == self.exit:
            return self.theme["exit"]
        elif not self.hide_solution and cell in self.solution:
            return self.theme["path"]
        elif self.forty_two and cell in self.forty_two:
            return self.theme["fortytwo"]
        else:
            return "  "

    def wall_content(self, curr_cell: tuple[int, int], last_cell: tuple[int, int]) -> str:
        if not self.hide_solution and curr_cell in self.solution and last_cell in self.solution:
            return self.theme["path"]
        else:
            return "  "

    def top_line(self, y: int) -> str:
        top: str = ""
        for x in range(self.width):
            top += self.theme["wall"]
            if self.forty_two and (x, y) in self.forty_two and (x, y - 1) in self.forty_two:
                top += self.theme["fortytwo"]
            elif self.maze[y][x] & NORTH:
                top += self.theme["wall"]
            else:
                top += self.wall_content((x, y), (x, y - 1))
        top += self.theme["wall"]
        return top

    def mid_lane(self, y: int) -> str:
        mid: str = ""
        for x in range(self.width):
            if self.forty_two and (x, y) in self.forty_two and (x-1, y) in self.forty_two:
                mid += self.theme["fortytwo"]
            elif self.maze[y][x] & WEST:
                mid += self.theme["wall"]
            else:
                mid += self.wall_content((x, y), (x - 1, y))
            mid += self.cell_content(cell=(x, y))
        mid += self.theme["wall"]
        return mid

    def bottom_line(self) -> str:
        bot: str = ""
        for _ in range(self.width):
            bot += str(self.theme["wall"] + self.theme["wall"])
        bot += self.theme["wall"]
        return bot

    def render(self) -> None:
        for y in range(self.height):
            self.maze_str += self.top_line(y) + "\n"
            self.maze_str += self.mid_lane(y) + "\n"
        self.maze_str += self.bottom_line()

    def image_output(self) -> None:
        self.render()
        img = Image.new("RGB", (800, 600), "black")
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), self.maze_str, fill="white")
        img.save("maze.png")

    def display(self) -> None:
        self.render()
        print(self.maze_str)
