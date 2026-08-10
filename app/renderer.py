"""
Terminal Renderer Module.
Handles ASCII/Unicode grid visualization for the terminal interface with
Classic Arcade Green styling.
"""

from mazegen import Grid, Direction, Cell


class TerminalRenderer:
    """
    Renders Grid domain models to the terminal stdout.

    [Design Pattern: View Component in MVC]
    - Role: Concrete View / Terminal Renderer
    - Purpose: Format cell wall bitmask states into visual terminal ASCII box
      graphics, remaining isolated from generation and grid logic
    """

    RESET = "\033[0m"
    BOLD = "\033[1m"

    CORNER_COLOR = "\033[92m"
    WALL_COLOR = "\033[92m"
    ENTRY_COLOR = "\033[93m"
    EXIT_COLOR = "\033[91m"
    PATH_COLOR = "\033[97m"

    def render(
        self,
        grid: Grid,
        use_color: bool = False,
        entry: tuple[int, int] | None = None,
        exit_pos: tuple[int, int] | None = None,
        path: list[Cell] | None = None,
    ) -> None:
        """
        Renders the entire grid to standard output using ASCII box drawing.
        """
        c_reset = self.RESET if use_color else ""
        c_wall = self.WALL_COLOR if use_color else ""
        c_corner = self.CORNER_COLOR if use_color else ""
        c_entry = f"{self.ENTRY_COLOR}{self.BOLD}" if use_color else ""
        c_exit = f"{self.EXIT_COLOR}{self.BOLD}" if use_color else ""
        c_path = self.PATH_COLOR if use_color else ""

        path_coords = set()
        if path:
            path_coords = {(cell.row, cell.col) for cell in path}

        output_buffer: list[str] = []

        # Correct Top Border Construction
        top_parts = [f"{c_corner}+{c_reset}"]
        for _ in range(grid.width):
            top_parts.append(f"{c_wall}---{c_reset}{c_corner}+{c_reset}")
        output_buffer.append("".join(top_parts))

        for row in range(grid.height):
            cell_line_parts = [f"{c_wall}|{c_reset}"]
            bottom_line_parts = [f"{c_corner}+{c_reset}"]

            for col in range(grid.width):
                cell = grid.get_cell(row, col)
                if cell is None:
                    continue

                coord = (row, col)

                # Determine cell contents
                if entry and coord == entry:
                    cell_content = f"{c_entry} E {c_reset}"
                elif exit_pos and coord == exit_pos:
                    cell_content = f"{c_exit} X {c_reset}"
                elif coord in path_coords:
                    cell_content = f"{c_path} ★ {c_reset}"
                else:
                    cell_content = "   "

                cell_line_parts.append(cell_content)

                # East wall check
                if cell.has_wall(Direction.EAST):
                    cell_line_parts.append(f"{c_wall}|{c_reset}")
                else:
                    cell_line_parts.append(" ")

                # South wall check
                if cell.has_wall(Direction.SOUTH):
                    bottom_line_parts.append(f"{c_wall}---{c_reset}{c_corner}+{c_reset}")
                else:
                    bottom_line_parts.append(f"   {c_corner}+{c_reset}")

            output_buffer.append("".join(cell_line_parts))
            output_buffer.append("".join(bottom_line_parts))

        # Print whole grid in a single stream flush
        print("\n".join(output_buffer))