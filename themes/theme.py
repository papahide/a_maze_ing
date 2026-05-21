import random


class MazeTheme:
    def __init__(self) -> None:
        self.wall_color: str = "██"
        self.path_color: str = "\033[33m██\033[0m"
        self.f_t_color: str = "\033[38;5;253m██\033[0m"
        self.entry_color: str = ""
        self.exit_color: str = ""
        self.custom_path: str = ""

    # RESET
    RESET = "\033[0m"

    # BASIC
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"

    # BRIGHT
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_WHITE = "\033[97m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_MAGENTA = "\033[95m"

    # 256 COLORS
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[38;5;93m"
    PINK = "\033[38;5;213m"
    TURQUOISE = "\033[38;5;45m"
    GOLD = "\033[38;5;220m"
    LAVENDER = "\033[38;5;183m"
    SALMON = "\033[38;5;209m"
    MINT = "\033[38;5;121m"
    PEACH = "\033[38;5;216m"
    CORAL = "\033[38;5;203m"
    SKY_BLUE = "\033[38;5;117m"
    VIOLET = "\033[38;5;177m"

    def rand_color(self) -> str:
        colors: list[str] = [
            self.CYAN,
            self.MAGENTA,
            self.WHITE,
            self.BRIGHT_BLACK,
            self.BRIGHT_WHITE,
            self.BRIGHT_CYAN,
            self.BRIGHT_MAGENTA,
            self.ORANGE,
            self.PURPLE,
            self.PINK,
            self.TURQUOISE,
            self.GOLD,
            self.LAVENDER,
            self.SALMON,
            self.MINT,
            self.PEACH,
            self.CORAL,
            self.SKY_BLUE,
            self.VIOLET
        ]
        return random.choice(colors) + "██" + self.RESET
