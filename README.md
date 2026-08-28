_This activity has been created as part of the 42 curriculum by borabi, hqasqas._

# A-Maze-ing 🧩

A procedural maze generation, solving, and terminal visualization engine built in Python. Designed as a clean, modular library, **A-Maze-ing** generates mazes based on custom configuration files, solves optimal paths using Breadth-First Search (BFS), and renders ANSI-colored grids directly to the terminal.

---

## 📋 Description

The goal of **A-Maze-ing** is to build a robust, object-oriented maze generation and pathfinding engine that enforces strict separation of concerns through design patterns (MVC, Strategy Pattern).

### Key Features

- **Configurable Generation:** Parses custom configuration files defining grid dimensions, entry/exit coordinates, output path, perfect/imperfect modes, and pattern masks.
- **Algorithmic Pathfinding:** Calculates shortest-path navigation using Breadth-First Search (BFS) and outputs directional path strings (`N`, `E`, `S`, `W`).
- **Classic Arcade Terminal Renderer:** Renders ASCII grid displays with ANSI escape codes (Classic Arcade Green palette) without external dependencies.
- **'42' Pattern Masking:** Automatically blocks out central grid cells in the shape of the '42' logo for sufficiently large grids.
- **Imperfect Mazes (`PERFECT=False`):** Carves secondary passages to form Pac-Man-style loops and multiple solution paths.
- **Reusable Core Engine:** Distributed as a standalone, pip-installable wheel package (`mazegen-*.whl`).

---

## ⚙️ Configuration File Format

The application accepts configuration files formatted with one `KEY=VALUE` pair per line.

### Complete Structure & Supported Keys

| Key           | Type    | Description                                                 | Default               |
| :------------ | :------ | :---------------------------------------------------------- | :-------------------- |
| `WIDTH`       | `int`   | Grid width in cells                                         | Required              |
| `HEIGHT`      | `int`   | Grid height in cells                                        | Required              |
| `ENTRY`       | `tuple` | Starting coordinates `(row, col)`                           | `(0, 0)`              |
| `EXIT`        | `tuple` | Ending coordinates `(row, col)`                             | `(height-1, width-1)` |
| `OUTPUT_FILE` | `str`   | Target output path for generated maze solution              | `output_maze.txt`     |
| `PERFECT`     | `bool`  | `True` for perfect mazes (spanning tree), `False` for loops | `False`               |
| `SEED`        | `int`   | Optional seed for reproducible generation                   | Random                |

### Sample `config.txt`

```text
HEIGHT=15
WIDTH=20
ENTRY=0,0
EXIT=14,19
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

When `SEED` is provided, the same configuration produces the same maze layout.

## 🚀 Instructions

### Prerequisites

- Python 3.10 or higher
- Poetry package manager
- GNU `make`

### Installation

Clone the repository and install all virtual environment dependencies:

```bash
make install
```

### Execution

Run the main application using a configuration file:

```bash
make run
```

### Development, Testing & Code Quality

- **Run Tests with Coverage:**
  ```bash
  make debug
  ```
- **Run Type Checking & Linting (MyPy & Flake8):**
  ```bash
  make lint
  ```
- **Build Reusable Wheel Package:**
  ```bash
  make build
  ```
- **Clean Build Caches:**
  ```bash
  make clean
  ```

---

## 🧮 Maze Generation Algorithm

### Algorithm Chosen: Randomized Depth-First Search (Recursive Backtracker)

We selected **Randomized Depth-First Search (DFS)** as our core spanning-tree generation algorithm.

### Why We Chose DFS

1. **Long, Winding Passages:** DFS produces mazes with a high "river" factor—long, twisted corridors and deep dead-ends—creating visually striking and challenging mazes compared to uniform algorithms like Kruskal's or Prim's.
2. **Stack-Based Efficiency:** It operates with memory complexity proportional to the grid size on the call stack or an explicit stack structure, making it memory-efficient for large grids.
3. **Simple Mask Integration:** Backtracking naturally respects masked/disabled cells (such as the '42' pattern mask) by treating them as visited or impassable boundaries.

---

## 🏗️ Architecture & Design Patterns

To ensure the library is maintainable and reusable, we strictly adhered to standard software design patterns:

### MVC-Inspired Architecture

The project separates responsibilities into distinct layers:

- **Model:** `mazegen/grid.py`, `mazegen/cell.py` — manages the maze state, cells, walls, and boundaries.
- **Algorithms:** `mazegen/` — contains maze generation and solving algorithms.
- **Input:** `app/parser.py` — parses and validates user configuration.
- **Controller:** `a_maze_ing.py` — orchestrates the application flow and coordinates the other components.
- **View/Output:** `app/renderer.py`, `app/writer.py` — handles terminal rendering and file output.

This separation keeps the maze logic independent from input handling and presentation.

### Strategy Pattern

We utilized the **Strategy Pattern** via Python Abstract Base Classes (`abc.ABC`) to make algorithms interchangeable:

- **Generators:** A `BaseGenerator` interface defines how a generator should behave. Our `MazeGenerator` implements DFS strategy. If a future developer wants to add Kruskal's or Prim's algorithm, they simply create a new strategy class without altering the core controller.
- **Solvers:** A `BaseSolver` interface handles pathfinding. We implemented the `BFSSolver` strategy, but this design allows for seamless integration of an `AStarSolver` or `DijkstraSolver` in the future.

---

## 📦 Reusable Code & Package Integration

The project is structured into two distinct packages:

- **`mazegen/` (Reusable Library Core):** Contains pure domain logic independent of any CLI or terminal display (`Grid`, `Cell`, `BaseGenerator`, `MazeGenerator`, `BaseSolver`, `BFSSolver`).
- **`app/` (Application Layer):** Handles CLI configuration parsing, terminal rendering, and file output formatting.

### How to Reuse `mazegen` in Future Projects

You can install the pre-built wheel artifact directly into any Python project:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

#### Code Integration Example:

```python
from mazegen import Grid, MazeGenerator, BFSSolver

# 1. Initialize Grid
grid = Grid(width=15, height=10)

# 2. Generate Maze
generator = MazeGenerator()
generator.generate(grid, start_row=0, start_col=0)

# 3. Solve Path
solver = BFSSolver()
path = solver.solve(grid, entry=(0, 0), exit_pos=(9, 14))
```

---

## 👥 Team & Project Management

### Team Roles

- **`borabi` (Bilal Orabi):**
  - **Designed the modular repository structure** and project architecture, Poetry dependency configuration, package layout.
  - **Core grid models** (`Grid`, `Cell`, bitmask direction utilities).
  - **Pathfinding engine** (`BaseSolver`, `BFSSolver` strategy, cardinal string generation).
  - **Maze generation engine** (`BaseGenerator`, `MazeGenerator` strategy, recursive backtracking logic).
  - **Packaging**, `pyproject.toml` metadata, `LICENSE.md`, `Makefile` build targets, and project documentation.

- **`hqasqas` (Hamza Nabil):**
  - **developed terminal renderer extensions and output file formatting** ensuring clean resource management through context managers and safe file handling.
  - **Config file parser** (`ConfigParser`) and ANSI Terminal Renderer
  - **'42' pattern mask implementation** and `PERFECT=False` loop generator adjustments.
  - **Implemented comprehensive unit test suites** using `pytest` and `pytest-cov`, ensuring robust coverage.

### Planning Evolution

- **Anticipated Schedule:**
  - _Week 1:_ Architecture design, grid domain model, and config parser.
  - _Week 2:_ Generation algorithms, BFS pathfinder, and terminal display.
  - _Week 3:_ '42' mask implementation, imperfect maze loops, packaging, and defense preparation.
- **Actual Timeline:**
  - Core domain models, parser, and generator logic progressed faster than scheduled due to early test coverage.
  - More time was allocated to fine-tuning terminal ANSI color contrast and ensuring zero-dependency

### What Worked Well & What Could Be Improved

- **What Worked Well:**
  - **Modular Architecture:** Strict adherence to domain isolation (`mazegen` vs `app`) allowed us to develop generator logic, terminal rendering, and solver strategies in parallel without git conflicts.
  - **Test-Driven Workflows:** Maintaining high unit test coverage with `pytest` caught edge cases early.
  - **Continuous Integration (CI):** Setting up an automated CI workflow was a game-changer. Having our unit tests (`pytest`), linters (`flake8`), and type checks (`mypy`) run automatically on every push ensured that our `main` branch remained stable and bug-free.
- **What Could Be Improved:**
  - **Algorithm Expansion:** While DFS and BFS met our core requirements perfectly, adding more Strategy classes (like Kruskal's for generation or A\* for pathfinding) would allow for interesting visual and performance comparisons.

### Tools Used

- **Dependency management & Packaging & Build system:** Poetry
- **Version Control:** Git, GitHub
- **Testing & Quality Assurance:** `pytest`, `pytest-cov`, `mypy` (strict mode), `flake8`
- **Text Editor / IDE:** VSCode

---

## 📚 Resources

### References & Documentation

- **Python official documentation**
- **Maze Generation Algorithms:** Jamis Buck - Buckblog Maze Algorithms
- **Pathfinding & BFS:** Red Blob Games - Introduction to A\* and BFS
- **ANSI Escape Codes:** Build your own Command Line Interface with ANSI escape codes

### AI Usage

Artificial Intelligence was utilized during this project for the following specific tasks:

1. **Architectural Review:** Validating Strategy Pattern implementations for `BaseGenerator` and `BaseSolver`.
2. **Terminal Rendering Optimization:** Designing ANSI color palette schemes.
3. **Build Automation:** Designing cross-platform `Makefile` targets and verifying PEP 621 compliance in `pyproject.toml`.
4. **Unit Testing Assistance:** Leveraging AI to generate `pytest` boilerplate and brainstorm tricky edge cases.
   All AI-suggested tests were manually verified, executed, and tuned to match our domain models.
