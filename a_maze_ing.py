import sys
import src
import errors
# import curses


def get_interaction(decision: int) -> None:
    pass


def get_parsed_configuration(conf_file: str) -> src.MazeConfig:
        parser: src.MazeParsing = src.MazeParsing()
        conf_content: str = parser.conf_read(conf_file)
        conf: src.MazeConfig = parser.config_parse(conf_content,
                                                   str(sys.argv[1]))
        return conf


def display_default_maze(conf: src.MazeConfig) -> None:
    maze = src.MazeGenerator(conf)
    solution = src.MazeSolution(maze, conf.entry_point,
                                conf.exit_point)
    output = src.HexOutput(maze, maze.entry, maze.exit,
                           solution.directions, conf)
    maze.maze_gen()
    solution.solve()
    output.hex_output()
    maze_display = src.MazeRender(maze, conf, solution)
    maze_display.display()


def main() -> None:
    argn: int = len(sys.argv)
    if argn != 2:
        sys.stderr.write("No config file provided."
                         "Usage: python3 a_maze_ing.py "
                         "[configuration file].txt\n")
        sys.exit(1)
    try:
        conf: src.MazeConfig = get_parsed_configuration(sys.argv[1])
    except errors.MazeConfigError as m_err:
        sys.stderr.write(str(m_err) + "\n")
        sys.exit(1)
    display_default_maze(conf)
    # while True:
    #     print("\n=== A_MAZE_ING ===")
    #     print("r --> Regenerate maze")
    #     print("p --> Show/Hide path from entry to exit")
    #     print("c --> Change maze colors")
    #     print("e --> Custom path")
    #     print("q --> Quit")
    #     decision: int = int(input("Chouse a option: "))
    #     if decision == 5:
    #         break
    #     get_interaction(decision)


if __name__ == "__main__":
    main()
