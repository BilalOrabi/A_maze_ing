"""
A-Maze-ing Main Application Controller.

[Design Pattern: Controller Component in MVC]
- Role: Main Application Controller
- Purpose: Orchestrates configuration ingestion, model initialization,
  generator strategy execution, file exporting, and view rendering.
"""

import sys
from app import ConfigParser, TerminalRenderer, MazeWriter
from mazegen import Grid, MazeGenerator, BFSSolver
from mazegen import PatternMask


def main() -> None:
    """Main application controller entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "config.txt":
        config_file = sys.argv[1]
    elif len(sys.argv) == 1:
        print("you need to provide a configration file")
        return
    else:
        print("you have to make the same name file 'config.txt'")
        return

    # 1. Parse configuration
# 1. Parse configuration
    try:
        config = ConfigParser.parse(config_file)
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"Configuration error: {exc}")
        return

    # 2. Instantiate core domain model
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    grid = Grid(width=width, height=height)

    # 3. Extract coordinates
    entry: tuple[int, int] = config.get("ENTRY", (0, 0))
    exit_pos: tuple[int, int] = config.get("EXIT", (width - 1, height - 1))

    # 4. Apply the mandatory 42 pattern mask
    if not PatternMask.apply_42_mask(grid):
        print("Error: maze is too small for the 42 pattern.")
        return

    # 4. Generate maze using Strategy Pattern
    generator = MazeGenerator()
    generator.generate(grid, start_row=entry[0], start_col=entry[1])

    solver = BFSSolver()
    path = solver.solve(grid, entry, exit_pos)

    # 5. Export output file with full parameters
    output_path = str(config.get("OUTPUT_FILE", "output_maze.txt"))
    path_str = BFSSolver.path_to_directions(path)
    MazeWriter.write(grid, output_path, entry, exit_pos, path_str)

    renderer = TerminalRenderer()
    renderer.render(
        grid,
        use_color=True,
        entry=entry,
        exit_pos=exit_pos,
        path=path,
    )


if __name__ == "__main__":
    main()
