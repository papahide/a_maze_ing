from .maze_generation import MazeGenerator
from .maze_solution import MazeSolution
from themes.theme import MazeTheme
from errors import MazeGenError
from .hex_output import HexOutput
from .parser import MazeConfig
from .maze_render import MazeRender
from random import randint
from dataclasses import replace
import sys


class UserInteractions():
    """
    Class that manages the user interactions in the main program.
    """
    def __init__(self, conf: MazeConfig, maze: MazeGenerator,
                 solution: MazeSolution) -> None:
        """
        UserInteraction class attributes.
        """
        self.maze_conf: MazeConfig = conf
        self.path_hide: bool = True
        self.default_theme: dict[str,
                                 str] = {"wall": "██",
                                         "path": "\033[32m██\033[0m",
                                         "entry": "\033[33m██\033[0m",
                                         "exit": "\033[31m██\033[0m",
                                         "fortytwo": "\033[34m██\033[0m"}
        self.maze_theme: dict[str, str] = self.default_theme.copy()
        self.maze: MazeGenerator = maze
        self.solution: MazeSolution = solution

    def _regen_maze(self) -> None:
        """
        Class that regenerates the maze using the same or different seed.
        """
        regen_conf = replace(self.maze_conf, seed=randint(0, 9999))
        self.maze_conf = regen_conf
        self.maze = MazeGenerator(self.maze_conf)
        self.maze.maze_gen()
        self.solution = MazeSolution(self.maze, self.maze_conf.entry_point,
                                     self.maze_conf.exit_point)
        self.solution.solve()
        output = HexOutput(self.maze, self.maze.entry, self.maze.exit,
                           self.solution.directions, self.maze_conf)
        output.hex_output()
        maze_display = MazeRender(self.maze, self.maze_conf, self.solution,
                                  self.maze_theme, self.path_hide)
        maze_display.display()

    def _rerender(self) -> None:
        """
        Rerenders the maze with same seed.
        """
        maze_display = MazeRender(self.maze, self.maze_conf, self.solution,
                                  self.maze_theme, self.path_hide)
        maze_display.display()

    def _path_show_hide(self) -> None:
        """
        Hides/shows the solution path in the maze and renders
        it with same seed.
        """
        self.path_hide = not self.path_hide
        self._rerender()

    def _random_colors(self, color: MazeTheme) -> None:
        """
        Selects random colors for the maze walls, solution path and
        fortytwo central pattern.
        """
        self.maze_theme["wall"] = color.rand_colors()[0]
        self.maze_theme["path"] = color.rand_colors()[1]
        self.maze_theme["fortytwo"] = color.rand_colors()[2]

    def _custom_theme(self, color: MazeTheme) -> str:
        """
        Makes the user choose a predetermined theme for the maze.
        """
        themes: list[dict[str, str]] = color.get_theme_options()
        for i, theme in enumerate(themes):
            print("  -- NAME: WALL - PATH - CENTRAL PATTERN --")
            print(f'  {i + 1} -> {theme["name"]} : {theme["wall"]} - '
                  f'{theme["path"]} - {theme["fortytwo"]}')
        try:
            th_choice: int = int(input("  Choose a theme: ")) - 1
        except ValueError as err:
            sys.stderr.write(f"Input error: {err}\n")
            return "continue"
        if th_choice >= 0 and th_choice < len(themes):
            self.maze_theme = themes[th_choice]
            return "break"
        else:
            sys.stderr.write("Choose a valid option\n")
            return "continue"

    def _set_default_theme(self) -> None:
        """
        Sets the theme of the maze to default.
        """
        self.maze_theme = self.default_theme.copy()

    def _maze_colors(self) -> None:
        """
        Changes the colors of the maze.
        """
        color: MazeTheme = MazeTheme()
        while True:
            print("  1 -> Choose a theme"
                  "\n  2 -> Random theme"
                  "\n  3 -> Default theme"
                  "\n  4 -> Return")
            try:
                theme_mode: int = int(input("  Choose a option: "))
            except ValueError as err:
                sys.stderr.write(f"Input error: {err}\n")
                continue
            if theme_mode == 1:
                theme: str = self._custom_theme(color)
                if theme == "continue":
                    continue
                elif theme == "break":
                    break
            elif theme_mode == 2:
                self._random_colors(color)
                break
            elif theme_mode == 3:
                self._set_default_theme()
                break
            elif theme_mode == 4:
                return
            else:
                print("Select a valid option, try again")
        self._rerender()

    def _manual_emoji(self, emojis: list[str]) -> str:
        """
        Lets the user select the emoji to be displayed on in the solution path.
        """
        for i, emoji in enumerate(emojis):
            print(f"  {i + 1} -> {emoji}")
        try:
            path_char: int = int(
                input("Choose a character to draw the solution path: ")
            ) - 1
        except ValueError as err:
            sys.stderr.write(f"Input error: {err}\n")
            return "continue"
        self.maze_theme["path"] = emojis[path_char]
        if path_char >= 0 and path_char <= len(emojis):
            return "break"
        else:
            raise MazeGenError(f"{path_char} is not a valid emoji, "
                               f"try again")

    def _custom_path(self) -> None:
        """
        Handles the interaction in which the user wants to change
        the emoji to display in the solution path.
        """
        big_char: list[str] = ["🔥", "✅", "❌", "⭐", "🌟",
                               "💎", "🟢", "🔴", "🟡", "🔵",
                               "🐑", "🦕", "🐉", "👾", "💀",
                               "👑", "⚡", "🌈", "🍀", "🎯",
                               "🚀", "🧩", "🎲", "🪐", "🛸",
                               "🧠", "🎮"]
        while True:
            print("  1 -> Choose a emoji"
                  "\n  2 -> Random path emoji"
                  "\n  3 -> Default path theme"
                  "\n  4 -> Return")
            try:
                path_theme: int = int(input("  Choose a option: "))
            except ValueError as err:
                sys.stderr.write(f"Input error: {err}\n")
                continue
            if path_theme == 1:
                ret: str = self._manual_emoji(big_char)
                if ret == "continue":
                    continue
                elif ret == "break":
                    break
            elif path_theme == 2:
                path_char = randint(0, len(big_char) - 1)
                self.maze_theme["path"] = big_char[path_char]
                break
            elif path_theme == 3:
                self.maze_theme["path"] = self.default_theme["path"]
                break
            elif path_theme == 4:
                return
            else:
                print("  Select a valid option, try again")
                continue
        self._rerender()

    def handle_interactions(self, decision: int) -> None:
        """
        Main user interactino handling method, calls other methods
        depending on the user decision.
        """
        if decision == 1:
            self._regen_maze()
        elif decision == 2:
            self._path_show_hide()
        elif decision == 3:
            self._maze_colors()
        elif decision == 4:
            self._custom_path()
        else:
            raise MazeGenError(f"{decision} is not a valid choice")
