"""
Terminal Renderer Module.
Handles ASCII/Unicode grid visualization for the terminal interface with
rotatable color themes and specific masking styles.
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

    # Define the 4 color theme palettes(Walls/Corners, Entry, Exit, Path, Logo)
    THEMES = [
        {
            "name": "Classic Arcade Green",
            "wall": "\033[92m",      # Bright Green
            "entry": "\033[93m",     # Yellow
            "exit": "\033[91m",      # Red
            "path": "\033[97m",      # White
            "logo": "\033[90m",      # Dark Grey blocks
        },
        {
            "name": "Cyberpunk Neon",
            "wall": "\033[95m",      # Neon Magenta
            "entry": "\033[96m",     # Cyan
            "exit": "\033[93m",      # Yellow
            "path": "\033[97m",      # White
            "logo": "\033[94m",      # Electric Blue blocks
        },
        {
            "name": "Deep Ocean",
            "wall": "\033[94m",      # Blue
            "entry": "\033[92m",     # Green
            "exit": "\033[35m",      # Magenta
            "path": "\033[96m",      # Cyan
            "logo": "\033[36m",      # Dark Cyan blocks
        },
        {
            "name": "Sunset Ember",
            "wall": "\033[91m",      # Bright Red/Orange
            "entry": "\033[93m",     # Yellow
            "exit": "\033[95m",      # Purple
            "path": "\033[97m",      # White
            "logo": "\033[33m",      # Dark Yellow/Brown blocks
        },
    ]

    def render(
        self,
        grid: Grid,
        theme_index: int = 0,
        use_color: bool = False,
        entry: tuple[int, int] | None = None,
        exit_pos: tuple[int, int] | None = None,
        path: list[Cell] | None = None,
    ) -> None:
        """
        Renders the entire grid to standard output using ASCII box drawing.
        """
        # Safely fall back to theme 0 if the index goes out of bounds
        theme = self.THEMES[theme_index % len(self.THEMES)]

        c_reset = self.RESET if use_color else ""
        c_wall = theme["wall"] if use_color else ""
        c_corner = theme["wall"] if use_color else ""
        c_entry = f"{theme['entry']}{self.BOLD}" if use_color else ""
        c_exit = f"{theme['exit']}{self.BOLD}" if use_color else ""
        c_path = theme["path"] if use_color else ""
        c_logo = theme["logo"] if use_color else ""

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
                elif cell.is_reserved:
                    # Highlight the '42' pattern blocks using foreground
                    cell_content = f"{c_logo}███{c_reset}"
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
                    bottom_line_parts.append(
                        f"{c_wall}---{c_reset}{c_corner}+{c_reset}")
                else:
                    bottom_line_parts.append(f"   {c_corner}+{c_reset}")

            output_buffer.append("".join(cell_line_parts))
            output_buffer.append("".join(bottom_line_parts))

        # Print whole grid in a single stream flush
        print("\n".join(output_buffer))
