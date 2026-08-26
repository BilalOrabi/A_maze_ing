"""
Pattern Mask Module.

Provides utilities for applying the mandatory "42" pattern
to a maze grid.
"""

from mazegen.grid import Grid


class PatternMask:
    """
    Applies predefined patterns to a maze grid.

    [Design Pattern: Utility / Helper]
    - Role: Grid Mask Applicator
    - Purpose: Keeps the "42" pattern logic separate from the Grid
      data model and maze generation algorithms.
    """

    MASK_42: list[list[int]] = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]

    # Minimum required dimensions for applying the mask
    MIN_HEIGHT: int = 7
    MIN_WIDTH: int = 9

    @classmethod
    def can_fit_42(cls, grid: Grid) -> bool:
        """
        Check whether the "42" pattern can be placed safely.

        Besides geometric fit, keep one extra column of clearance so
        corridor cells near the "2" do not become landlocked in the
        minimum 7x9 layout.

        :param grid: Grid to check.
        :return: True if the pattern fits, otherwise False.
        """
        return (
            grid.height >= cls.MIN_HEIGHT
            and grid.width >= cls.MIN_WIDTH
        )

    @classmethod
    def apply_42_mask(cls, grid: Grid) -> bool:
        """
        Mark the cells forming the "42" pattern as reserved.

        Reserved cells are left untouched by the maze generator.
        Cells are initially created with all four walls closed, so
        reserved cells remain fully closed.

        :param grid: Grid that receives the "42" mask.
        :return: True if the mask was applied, False if it does not fit.
        """
        if not cls.can_fit_42(grid):
            return False

        mask_height = len(cls.MASK_42)
        mask_width = len(cls.MASK_42[0])

        start_row = (grid.height - mask_height) // 2
        start_col = (grid.width - mask_width) // 2

        for mask_row in range(mask_height):
            for mask_col in range(mask_width):
                if cls.MASK_42[mask_row][mask_col] != 1:
                    continue

                row = start_row + mask_row
                col = start_col + mask_col

                cell = grid.get_cell(row, col)
                if cell is not None:
                    cell.is_reserved = True

        return True
