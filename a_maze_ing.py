import sys
import src
import errors


def get_parsed_configuration(conf_file: str) -> src.MazeConfig:
    parser: src.MazeParsing = src.MazeParsing()
    conf_content: str = parser.conf_read(conf_file)
    conf: src.MazeConfig = parser.config_parse(conf_content,
                                               str(sys.argv[1]))
    return conf


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
    maze = src.MazeGenerator(conf)
    maze.maze_gen()
    solution = src.MazeSolution(maze, conf.entry_point,
                                conf.exit_point)
    solution.solve()
    output = src.HexOutput(maze, maze.entry, maze.exit,
                           solution.directions, conf)
    output.hex_output()
    maze_display = src.MazeRender(maze, conf, solution)
    maze_display.display()
    interaction: src.UserInteractions = src.UserInteractions(conf, maze, solution)
    while True:
        print("\n=== A_MAZE_ING ===")
        print("1 --> Regenerate maze")
        print("2 --> Show/Hide path from entry to exit")
        print("3 --> Change maze colors")
        print("4 --> Custom path")
        print("5 --> Quit")
        try:
            decision: int = int(input("Choose a option: "))
        except ValueError as err:
            sys.stderr.write(f"Input error: {err}\n")
            continue
        if decision == 5:
            break
        try:
            interaction.handle_interactions(decision)
        except errors.MazeGenError as err:
            sys.stderr.write(str(err) + "\n")


if __name__ == "__main__":
    main()
