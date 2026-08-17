"""
A-Maze-ing Main Application Controller.

[Design Pattern: Controller Component in MVC]
- Role: Main Application Controller
- Purpose: Orchestrates configuration ingestion, model initialization,
  generator strategy execution, file exporting, and view rendering.
"""

import sys
from app import ConfigParser, MazeWriter
from app.menu import InteractiveMenu
from mazegen import Grid, MazeGenerator, BFSSolver
from mazegen import PacmanModifier


def main() -> None:
    """Main application controller entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    config_file = sys.argv[1]

    # 1. Parse configuration
    try:
        config = ConfigParser.parse(config_file)
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"Configuration error: {exc}")
        return

    # 2. Instantiate core domain model
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    perfect: bool = config["PERFECT"]
    grid = Grid(width=width, height=height)
    seed: int | None = config.get("SEED")

    # 3. Extract coordinates
    entry: tuple[int, int] = config.get("ENTRY", (0, 0))
    exit_pos: tuple[int, int] = config.get("EXIT", (width - 1, height - 1))

    # 4. Generate maze initial layout using Strategy Pattern
    generator = MazeGenerator()
    try:
        # The generator applies the mask internally
        generator.generate(
            grid,
            start_row=entry[0],
            start_col=entry[1],
            exit_row=exit_pos[0],
            exit_col=exit_pos[1],
            seed=seed,
            apply_42=True,
        )
    except ValueError as exc:
        print(f"Generation error: {exc}")
        return

    # 5. Check if the mask swallowed the exit post-mask allocation
    exit_cell = grid.get_cell(exit_pos[0], exit_pos[1])
    if exit_cell and exit_cell.is_reserved:
        print(
            "Error: The EXIT coordinate cannot be inside the '42' pattern "
            "mask."
        )
        return

    # Apply Pac-Man modifications for non-perfect mazes
    if not perfect:
        PacmanModifier.open_corners(grid)
        PacmanModifier.open_center(grid)
        PacmanModifier.add_loops(grid)
        PacmanModifier.reduce_dead_ends(grid)

    # 6. Hand off control to the Chapter 5 Interactive Menu
    interactive_menu = InteractiveMenu(
        grid,
        entry,
        exit_pos,
        perfect,
        )
    interactive_menu.run()

    # 7. Export final file state upon cleanly exiting the interactive menu
    output_path = str(config.get("OUTPUT_FILE", "output_maze.txt"))
    solver = BFSSolver()
    final_path = solver.solve(grid, entry, exit_pos)
    path_str = BFSSolver.path_to_directions(final_path)
    MazeWriter.write(grid, output_path, entry, exit_pos, path_str)


if __name__ == "__main__":
    main()
