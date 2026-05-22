import random


class MazeTheme:
    def __init__(self) -> None:
        self.default_theme: dict[str, str] = {"wall": "██",
                                              "path": "\033[32m██\033[0m",
                                              "entry": "\033[33m██\033[0m",
                                              "exit": "\033[31m██\033[0m",
                                              "fortytwo": "\033[34m██\033[0m"}
    # RESET
    RESET = "\033[0m"

    # Diccionario de colores
    COLORS: dict[str, str] = {
        "cyan": "\033[36m",
        "magenta": "\033[35m",
        "white": "\033[37m",

        "bright_black": "\033[90m",
        "bright_white": "\033[97m",
        "bright_cyan": "\033[96m",
        "bright_magenta": "\033[95m",

        "orange": "\033[38;5;208m",
        "purple": "\033[38;5;93m",
        "pink": "\033[38;5;213m",
        "turquoise": "\033[38;5;45m",
        "gold": "\033[38;5;220m",
        "lavender": "\033[38;5;183m",
        "salmon": "\033[38;5;209m",
        "mint": "\033[38;5;121m",
        "peach": "\033[38;5;216m",
        "coral": "\033[38;5;203m",
        "sky_blue": "\033[38;5;117m",
        "violet": "\033[38;5;177m"
    }

    def rand_colors(self, amount: int = 3) -> list[str]:

        selected_colors = random.sample(
            list(self.COLORS.values()),
            amount
        )

        return [
            color + "██" + self.RESET
            for color in selected_colors
        ]

    def get_theme_options(self) -> list[dict[str, str]]:
        theme_options: list[dict[str, str]] = [
            {
                "name": "ICE / CYBER",
                "wall": "██",
                "path": "\033[96m██\033[0m",
                "entry": "\033[38;5;220m██\033[0m",
                "exit": "\033[38;5;203m██\033[0m",
                "fortytwo": "\033[38;5;117m██\033[0m"
            },
            {
                "name": "SUNSET",
                "wall": "██",
                "path": "\033[38;5;209m██\033[0m",
                "entry": "\033[38;5;220m██\033[0m",
                "exit": "\033[35m██\033[0m",
                "fortytwo": "\033[38;5;213m██\033[0m"
            },
            {
                "name": "FOREST",
                "wall": "██",
                "path": "\033[38;5;121m██\033[0m",
                "entry": "\033[38;5;216m██\033[0m",
                "exit": "\033[38;5;208m██\033[0m",
                "fortytwo": "\033[36m██\033[0m"
            },
            {
                "name": "DREAM / VAPORWAVE",
                "wall": "██",
                "path": "\033[38;5;183m██\033[0m",
                "entry": "\033[95m██\033[0m",
                "exit": "\033[38;5;45m██\033[0m",
                "fortytwo": "\033[38;5;177m██\033[0m"
            },
            {
                "name": "SPACE / NEON",
                "wall": "██",
                "path": "\033[38;5;93m██\033[0m",
                "entry": "\033[97m██\033[0m",
                "exit": "\033[38;5;203m██\033[0m",
                "fortytwo": "\033[96m██\033[0m"
            }
        ]
        return theme_options
