# mazegen

Standalone, reusable maze generation and solving library.

---

## Installation

Install directly from the distributed package file at the root of this repository:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or from the source tarball:

```bash
pip install mazegen-1.0.0.tar.gz
```

### Build from source (inside a virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install hatchling build
python3 -m build --outdir .
```

This produces `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the root of the repository.

---

## Quickstart

```python
from mazegen import MazeGenerator, MazeConfig, MazeSolution

# 1. Configure the maze
conf = MazeConfig(
    width=20,
    height=15,
    entry_point=(0, 0),
    exit_point=(19, 14),
    output_file="",       # unused when importing as a library
    perfect=True,         # False adds extra passages (imperfect maze)
    seed=42               # any int; use random.randint(0, 9999) for random
)

# 2. Generate the maze
gen = MazeGenerator(conf)
gen.maze_gen()

# 3. Solve the maze
sol = MazeSolution(gen, conf.entry_point, conf.exit_point)
sol.solve()

# 4. Read the results
print("Path length :", len(sol.path))       # number of cells in solution
print("Directions  :", sol.directions)       # e.g. "EESSWWNNE..."
print("Path cells  :", sol.path[:5])         # list of (x, y) tuples
```

---

## Custom Parameters

### `MazeConfig` fields

| Field | Type | Description |
|---|---|---|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry_point` | `tuple[int, int]` | `(x, y)` of the maze entrance |
| `exit_point` | `tuple[int, int]` | `(x, y)` of the maze exit |
| `output_file` | `str` | Path for file output (leave `""` when used as a library) |
| `perfect` | `bool` | `True` = perfect maze (one solution); `False` = extra passages |
| `seed` | `int` | RNG seed for reproducibility |

> **Note:** `entry_point` and `exit_point` must be different.  
> For the 42 pattern to appear, the maze must be at least 13 × 11 cells.

---

## Accessing the Generated Structure

After calling `gen.maze_gen()`, the raw maze is available as:

```python
gen.maze  # list[list[int]] — 2D grid, one int per cell
```

Each cell is a 4-bit integer where each bit represents a wall:

| Constant | Value | Wall |
|---|---|---|
| `NORTH` | `0b0001` | Top wall |
| `EAST` | `0b0010` | Right wall |
| `SOUTH` | `0b0100` | Bottom wall |
| `WEST` | `0b1000` | Left wall |

A bit set to `1` means the wall **exists**; `0` means it is **open**.

```python
from mazegen import NORTH, EAST, SOUTH, WEST

cell = gen.maze[y][x]
if cell & NORTH:
    print("Wall to the north")
if not cell & EAST:
    print("Passage to the east")
```

---

## Accessing the Solution

After calling `sol.solve()`:

| Attribute | Type | Description |
|---|---|---|
| `sol.path` | `list[tuple[int, int]]` | Ordered list of `(x, y)` cells from entry to exit |
| `sol.directions` | `str` | Compact direction string, e.g. `"EESSWN"` (`N`/`E`/`S`/`W`) |
| `sol.explored` | `list[tuple[int, int]]` | All cells visited by BFS (useful for visualisation) |

```python
# Walk the solution step by step
for cell, direction in zip(sol.path, sol.directions):
    print(f"  {cell} → {direction}")
```

---

## Reproducibility

Passing the same `seed` always produces the same maze:

```python
conf_a = MazeConfig(width=10, height=10,
                    entry_point=(0,0), exit_point=(9,9),
                    output_file="", perfect=True, seed=7)

conf_b = MazeConfig(width=10, height=10,
                    entry_point=(0,0), exit_point=(9,9),
                    output_file="", perfect=True, seed=7)

gen_a = MazeGenerator(conf_a); gen_a.maze_gen()
gen_b = MazeGenerator(conf_b); gen_b.maze_gen()

assert gen_a.maze == gen_b.maze  # always True
```

---

## `pyproject.toml` reference

```toml
[project]
name = "mazegen"
version = "1.0.0"
description = "Standalone reusable maze generator"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling", "build"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["mazegen"]

[tool.hatch.build.targets.sdist]
include = ["mazegen/"]
```