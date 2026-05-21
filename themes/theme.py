
class MazeTheme:
    def __init__(self) -> None:
        self.wall_color: str = "██"
        self.path_color: str = "\033[33m██\033[0m"
        self.f_t_color: str = "\033[253m██\033[0m"
        self.entry_color: str = ""
        self.exit_color: str = ""
        self.custom_path: str = ""

    # RESET
    RESET = "\033[0m"

    # 10 colores combinables
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_BLUE = "\033[94m"

    def change_colors(self) -> list[str]:
        pass

    def get_custom_char(self) -> str:
        pass