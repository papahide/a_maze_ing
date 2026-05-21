from .maze_generation import MazeGenerator
from .maze_solution import MazeSolution
from themes.theme import MazeTheme
from errors import MazeGenError
from .hex_output import HexOutput
from .parser import MazeConfig
from .maze_render import MazeRender
from dataclasses import replace
from random import randint
import sys


class UserInteractions():
    def __init__(self, conf: MazeConfig, maze: MazeGenerator,
                 solution: MazeSolution) -> None:
        self.maze_conf: MazeConfig = conf
        self.path_hide: bool = True
        self.maze_theme: dict[str,
                              str] = {"wall": "██",
                                      "path": "\033[32m██\033[0m",
                                      "entry": "\033[33m██\033[0m",
                                      "exit": "\033[31m██\033[0m",
                                      "fortytwo": "\033[34m██\033[0m"}
        self.maze: MazeGenerator = maze
        self.solution: MazeSolution = solution

    def _regen_maze(self, regen: bool = True) -> None:
        if regen:
            regen_conf = replace(self.maze_conf, seed=randint(0, 9999))
            self.maze_conf = regen_conf
        else:
            regen_conf = self.maze_conf
        self.maze = MazeGenerator(regen_conf)
        self.maze.maze_gen()
        self.solution = MazeSolution(self.maze, regen_conf.entry_point,
                                    regen_conf.exit_point)
        self.solution.solve()
        output = HexOutput(self.maze, self.maze.entry, self.maze.exit,
                            self.solution.directions, regen_conf)
        output.hex_output()
        maze_display = MazeRender(self.maze, regen_conf, self.solution,
                                  self.maze_theme, self.path_hide)
        maze_display.display()

    def _path_show_hide(self) -> None:
        self.path_hide = not self.path_hide
        self._regen_maze(False)


    def _rerender(self) -> None:
        maze_display = MazeRender(self.maze, self.maze_conf, self.solution,
                                self.maze_theme, self.path_hide)
        maze_display.display()

    def _maze_colors(self) -> None:
        color: MazeTheme = MazeTheme()
        self.maze_theme["wall"] = color.rand_color()
        self._rerender()

    def _custom_path(self) -> None:
        big_char: list[str] = ["🔥", "✅", "❌", "⭐", "🌟",
                               "💎", "🟢", "🔴", "🟡", "🔵",
                               "🐑", "🦕", "🐉", "👾", "💀",
                               "👑", "⚡", "🌈", "🍀", "🎯",
                               "🚀", "🧩", "🎲", "🪐", "🛸",
                               "🧠","👁️", "🎮"]
        while True:
            print("  1 -> Choose a emoji"
                  "\n  2 -> Random path emoji" \
                  "\n  3 -> Default path theme" \
                  "\n  4 -> Return")
            try:
                man_or_rand: int = int(input("  Choose a option: "))
            except Exception as err:
                sys.stderr.write(f"Input error: {err}\n")
                continue
            if man_or_rand  == 1:
                for i, emoji in enumerate(big_char):
                    print(f"  {i + 1} -> {emoji}")
                try:
                    path_char: int = int(input("Choose a character to draw the solution path: ")) - 1
                except Exception as err:
                    sys.stderr.write(f"Input error: {err}\n")
                    continue
                self.maze_theme["path"] = big_char[path_char]
                if path_char >= 0 and path_char <= len(big_char):
                    break
                else:
                    raise MazeGenError(f"{path_char} is not a valid emoji, try again")
            elif man_or_rand == 2:
                path_char: int = randint(0, len(big_char) - 1)
                self.maze_theme["path"] = big_char[path_char]
                break
            elif man_or_rand == 3:
                self.maze_theme["path"] = "\033[32m██\033[0m"
                break
            elif man_or_rand == 4:
                return
            else:
                print(f"Select a valid option, try again")
        self._rerender()

    def handle_interactions(self, decision: int) -> None:
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
