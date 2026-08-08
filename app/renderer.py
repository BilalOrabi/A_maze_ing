"""
Terminal Renderer Module.

Handles ASCII/Unicode grid visualization for the terminal interface.

"""


from mazegen import Grid
from mazegen import Direction


class TerminalRenderer:
    """
    Renders Grid domain models to the terminal stdout.

    [Design Pattern: View Component in MVC]
    - Role: Concrete View / Terminal Renderer
    - Purpose: Format cell wall bitmask states into visual terminal ASCII box
      graphics, remaining isolated from generation and grid logic
    """

    def render(self, grid: Grid) -> None:

        """
        Renders the entire grid to standard output using ASCII box drawing.

        :param grid: Grid model instance to draw.
        """
        top_line: str = "+" + "---+" * grid.width
        print(top_line)
        for row in range(grid.height):
            cell_line = "|"
            bottom_line = "+"
            for col in range(grid.width):
                cell = grid.get_cell(row, col)
                if cell is None:
                    continue
                cell_line += "   "
                cell_line += "|" if cell.has_wall(Direction.EAST) else " "
                bottom_line += (
                    "---+" if cell.has_wall(Direction.SOUTH) else "   +"
                )
            print(cell_line)
            print(bottom_line)
