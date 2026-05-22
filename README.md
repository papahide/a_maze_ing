*This project was created as part of the 42 curriculum by \<paapahid>, \<clalfons\>.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. The program reads a configuration file, generates a random maze (reproducible via a seed), writes it to an output file in hexadecimal format along with the shortest solution path, and displays it visually in a graphical window using the MiniLibX library.

The maze can be **perfect** (a single path between entry and exit) or **imperfect** (multiple paths). In both cases it includes the **"42"** pattern drawn with fully closed cells in the center, provided the maze size allows it.

## Instructions

### Prerequisites

- Python 3.10 or higher
- OS: Ubuntu or Fedora (required for graphical rendering with MLX)

### Installation

```bash
make install
```

This installs all project dependencies, including the appropriate MiniLibX library for your system.

You can also install the MLX library manually:

```bash
# Ubuntu
pip install mlx-2_2-py3-ubuntu-any.whl

# Fedora
pip install mlx-2_2-py3-fedora-any.whl
```

### Running the program

```bash
python3 a_maze_ing.py configuration.txt
```

Or using the Makefile:

```bash
make run
```

### Makefile rules

```bash
make install      # Install dependencies
make run          # Run the program with configuration.txt
make debug        # Run in debug mode with pdb
make lint         # Run flake8 and mypy
make lint-strict  # Run mypy --strict
make clean        # Remove caches and temporary files
```

## Configuration file format

The configuration file is a plain text file with one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells (minimum 3) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (minimum 3) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y` (must be on the border) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y` (must be on the border) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output file name (`.txt`) | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect (`True`) or not (`False`) | `PERFECT=True` |
| `SEED` | Seed to reproduce a specific maze (optional) | `SEED=42` |

Example configuration file:

```
# Maze configuration
WIDTH=15
HEIGHT=15
ENTRY=0,4
EXIT=1,14
OUTPUT_FILE=conf.txt
PERFECT=False
# SEED=42
```

## Output file format

The output file contains:

1. The maze in hexadecimal, row by row (one hex digit per cell).
2. An empty line.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit, using the letters `N`, `E`, `S`, `W`.

Each hexadecimal digit encodes the walls of a cell as bits:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A bit set to `1` means the wall is closed, `0` means open. For example, `F` (binary `1111`) is a fully closed cell.

## Generation algorithm

The program uses **iterative DFS with backtracking** (also known as the *recursive backtracker*).

The algorithm starts from the entry cell with all walls closed and randomly carves passages using a stack, backtracking whenever there are no unvisited neighbours. The result is always a perfect maze (full spanning tree).

If `PERFECT=False`, a random 15% of interior walls are then removed while ensuring no 3×3 open zones are created.

**Why this algorithm?** It produces mazes with long, winding corridors that are visually interesting and fun to navigate. It is straightforward to implement iteratively, memory-efficient, and guarantees full connectivity, making it easy to satisfy all project requirements.

## Visualization

The program displays the maze in a graphical window using **ASCII rendering**. The entry is highlighted in magenta and the exit in red.

Available interactions:

| Key | Action |
|-----|--------|
| `1` | Regenerate a new maze |
| `2` | Show / hide the shortest path |
| `3` | Rotate wall colours |
| `4` / `ESC` | Quit |

## Reusable code — `mazegen` package

The generation logic is encapsulated in the `MazeGenerator` class inside the `src/maze_generation.py` module, packaged as `mazegen-*` and installable via pip.

### Package installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator, MazeConfig

config = MazeConfig(
    width=20,
    height=15,
    entry_point=(0, 0),
    exit_point=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42
)

generator = MazeGenerator(config)
generator.maze_gen()

# Access the maze structure
maze = generator.maze  # list[list[int]], one int per cell encoding N/E/S/W walls
```

### Custom parameters

```python
# Imperfect maze with a fixed seed
config = MazeConfig(
    width=30,
    height=20,
    entry_point=(0, 0),
    exit_point=(29, 19),
    output_file="out.txt",
    perfect=False,
    seed=1234
)
```

### Accessing the solution

```python
from mazegen import MazeGenerator, MazeSolution, MazeConfig

generator = MazeGenerator(config)
generator.maze_gen()

solution = MazeSolution(generator, config.entry_point, config.exit_point)
solution.solve()

print(solution.directions)  # e.g. "EESSWWNNE..."
print(solution.path)        # list of (x, y) cells forming the path
```

### Building the package from source

```bash
python3 -m pip install build
python3 -m build
```

This generates the `.whl` file in the `dist/` directory.

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — think-maths.co.uk](https://www.think-maths.co.uk/maze)
- [Spanning trees and perfect mazes](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [BFS for maze solving](https://en.wikipedia.org/wiki/Breadth-first_search)
- [MiniLibX Python — documentation included in `mlx_CLXV-2_2.tar`](mlx_CLXV/python/README.md)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy — Static Type Checker](https://mypy.readthedocs.io/)

### AI usage

AI was used as a support tool during development for the following tasks:

- Drafting and reviewing the `README.md` file.
- Assistance writing docstrings following PEP 257.
- Guidance on Python package structure (`pyproject.toml`, `build`).

All project code was written, reviewed and fully understood by the team members.

## Team and project management

### Roles

| Login | Main responsibility |
|-------|---------------------|
| `<paapahid>` | \<programmer\> |
| `<clalfons>` | \<programmer\> |

### Tools used

- Git / GitHub for version control
- Claude (Anthropic) for documentation