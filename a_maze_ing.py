"""
A-Maze-ing Main Application Controller.

[Design Pattern: Controller Component in MVC]
- Role: Main Application Controller
- Purpose: Orchestrates configuration ingestion, model initialization,
  generator strategy execution, file exporting, and view rendering.
"""

import sys
from app.parser import ConfigParser
from app.renderer import TerminalRenderer
from app.writer import MazeWriter
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator


def main() -> None:
    """Main application controller entry point."""
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"

    # 1. Parse configuration
    config = ConfigParser.parse(config_file)

    # 2. Instantiate core domain model
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    grid = Grid(width=width, height=height)

    # 3. Extract coordinates
    entry: tuple[int, int] = config.get("ENTRY", (0, 0))
    exit_pos: tuple[int, int] = config.get("EXIT", (width - 1, height - 1))

    # 4. Generate maze using Strategy Pattern
    generator = MazeGenerator()
    generator.generate(grid, start_row=entry[0], start_col=entry[1])

    # 5. Export output file with full parameters
    output_path = str(config.get("OUTPUT_FILE", "output.txt"))
    path_str = ""  # Placeholder string until Milestone 4 pathfinding engine
    MazeWriter.write(grid, output_path, entry, exit_pos, path_str)

    # 6. Render view
    renderer = TerminalRenderer()
    renderer.render(grid)


if __name__ == "__main__":
    main()
