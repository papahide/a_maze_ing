from dataclasses import dataclass
from errors import MazeConfigError
import random


@dataclass(frozen=True)
class MazeConfig:
    """
    DataClass to store all configurations + __post_init__ method.

    This dataclass contains all the parameters needed for the
    program to work.
    """
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int

    def __post_init__(self) -> None:
        """
        Performs additional validation after creating the object.

        The class uses __post_init__ to perform aditional validation
        after the object creation.
        """
        if self.entry_point == self.exit_point:
            raise MazeConfigError("The entry and exit points, "
                                  "cannot be the same")


class MazeParsing:
    """
    This class contains the parsing needed to run the program.
    """
    @staticmethod
    def conf_read(config_name: str) -> str:
        """
        Function that tryes to open the configuration file:
            - Raise error if there is a problem.
            - Return content if there is no errors.
        """
        if not config_name:
            raise MazeConfigError("No configuration file provided")
        try:
            with open(config_name, "r") as conf_file:
                content: str = conf_file.read()
                if not content:
                    raise MazeConfigError("No configuration provided")
                return str(content)
        except FileNotFoundError as err:
            raise MazeConfigError(f"Configuration file not found: {err}")
        except PermissionError as err:
            raise MazeConfigError(f"Configuration file insufficient "
                                  f"permissions: {err}")
        except IsADirectoryError as err:
            raise MazeConfigError(f"Configuration file not found, "
                                  f"'{config_name}' is a directory : {err}")

    @staticmethod
    def conf_keys_valid(raw_config: list[str]) -> None:
        """
        Validate that there is all the mandatory
        parameters in the configuration file.
        """
        required: list[str] = ["WIDTH", "HEIGHT",
                               "ENTRY", "EXIT",
                               "OUTPUT_FILE", "PERFECT"]
        for key in required:
            if key not in raw_config:
                raise MazeConfigError(f"Missing mandatory key: {key}")

    @staticmethod
    def conf_validation(content: str) -> dict[str, str]:
        """
        This function parses the configuration file removing leaps and
        returns a dictionary with [Key]:[Value].
        """
        lines: list[str] = [
            line.strip() for line in content.strip().split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        raw_config: dict[str, str] = {}
        for line in lines:
            if "=" not in line:
                raise MazeConfigError(f"Invalid format in line: {line}")
            if " " in line:
                raise MazeConfigError(f"Invalid format in line: {line}"
                                      "Usage: [Key]=[value]")
            key, value = line.split("=", 1)
            if key in raw_config:
                raise MazeConfigError(f"Duplicate key found: {key}")
            raw_config[key] = value
        MazeParsing.conf_keys_valid(list(raw_config.keys()))
        return raw_config

    @staticmethod
    def _parse_int(value: str, min_val: int |
                   None = None, max_val: int | None = None) -> int:
        """
        Validation and conversion form string to int.
        """
        try:
            parsed: int = int(value)
        except ValueError as err:
            raise MazeConfigError(f"Value error: {err}")
        if min_val is not None and parsed < min_val:
            raise MazeConfigError(f"Value must be >= {min_val}, got: {parsed}")
        if max_val is not None and parsed > max_val:
            raise MazeConfigError(f"Value must be <= {max_val}, got: {parsed}")
        return parsed

    @staticmethod
    def _parse_coord(coords: str, width: int, height: int) -> tuple[int, int]:
        """
        Validation and conversion fron string to coord: tuple[int, int]
        """
        coord_temp: list[str] = coords.split(",", 1)
        if len(coord_temp) != 2:
            raise MazeConfigError(f"Invalid coordinate format, "
                                  f"expected x,y: {coords}")
        try:
            x: int = int(coord_temp[0])
            y: int = int(coord_temp[1])
        except ValueError as err:
            raise MazeConfigError(f"Coordinates must be integers: {err}")
        if not (0 <= x < width and 0 <= y < height):
            raise MazeConfigError(f"Coordinates out of bounds, must be in "
                                  f"[0,{width - 1}] x [0,{height - 1}], "
                                  f"got: {coords}")
        return (x, y)

    @staticmethod
    def _validate_border(coords: tuple[int, int], width: int,
                         height: int, name: str) -> None:
        """
        Validates that the entry and exit points are stuck to a
        border of the maze.
        """
        x, y = coords
        if not (x == 0 or x == width - 1 or y == 0 or y == height - 1):
            raise MazeConfigError(f"{name} point is not valid, "
                                  f"must be at border of maze, got: {coords}")

    @staticmethod
    def _parse_bool(perfect: str) -> bool:
        """
        Validates and converts string to bool.
        """
        if perfect not in ("True", "False"):
            raise MazeConfigError(f"Incorrect \"perfect\" values, use: "
                                  f"True or False, got: {perfect}")
        return perfect == "True"

    @staticmethod
    def _parse_output_file(file: str, config_name: str) -> str:
        """
        Validates that the output file can be open and write in it.
        And creates one if there is no configuration file.
        """
        if not file:
            raise MazeConfigError("No output file provided")
        if not file.endswith(".txt"):
            raise MazeConfigError(f"File must be a *.txt, got: {file}")
        if file == config_name:
            raise MazeConfigError("Configuration file and output file have "
                                  "the same name: Change output file name")
        try:
            with open(file, "a"):
                pass
        except PermissionError as err:
            raise MazeConfigError(f"Invalid output file: {err}")
        except IsADirectoryError as err:
            raise MazeConfigError(f"Invalid output file: {err}")
        except OSError as err:
            raise MazeConfigError(f"Invalid output file: {err}")
        return file

    def config_parse(self, content: str, config_name: str) -> MazeConfig:
        """
        Main parse function.
        Uses previous functions to validate and parse data.
        Finally, returns all configuration file parameters stored
        in MazeConfig dataclass.
        """
        raw_config: dict[str, str] = self.conf_validation(content)
        width: int = self._parse_int(raw_config.get("WIDTH", ""), 3, 9999)
        height: int = self._parse_int(raw_config["HEIGHT"], 3, 9999)
        entry_point: tuple[int, int] = self._parse_coord(raw_config["ENTRY"],
                                                         width, height)
        exit_point: tuple[int, int] = self._parse_coord(raw_config["EXIT"],
                                                        width, height)
        output_file: str = self._parse_output_file(raw_config["OUTPUT_FILE"],
                                                   config_name)
        perfect: bool = self._parse_bool(raw_config["PERFECT"])
        seed: int = (
            self._parse_int(raw_config["SEED"])
            if "SEED" in raw_config else random.randint(0, 9999)
        )
        return MazeConfig(
            width=width,
            height=height,
            entry_point=entry_point,
            exit_point=exit_point,
            output_file=output_file,
            perfect=perfect,
            seed=seed
        )
