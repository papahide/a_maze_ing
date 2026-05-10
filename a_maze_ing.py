import sys
import src
import errors


def main() -> None:
    argn: int = len(sys.argv)
    if argn != 2:
        sys.stderr.write("No config file provided."
                         "Usage: python3 a_maze_ing.py "
                         "[configuration file].txt\n")
        sys.exit(1)
    try:
        conf_content: str = src.MazeParsing.conf_read(sys.argv[1])
        parser: src.MazeParsing = src.MazeParsing()
        conf: src.MazeConfig = parser.config_parse(conf_content,
                                                   str(sys.argv[1]))
    except errors.MazeConfigError as m_err:
        sys.stderr.write(str(m_err) + "\n")
        sys.exit(1)
    print(str(conf))


if __name__ == "__main__":
    main()
