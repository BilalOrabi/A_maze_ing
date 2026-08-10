"""
Pac-Man Maze Modifier.

Provides modifications required for PERFECT=False mazes.
"""

from mazegen import Direction, Grid


class PacmanModifier:
    """
    Modifies a generated maze for Pac-Man mode.

    [Design Pattern: Modifier / Post-Processing Component]
    - Role: Applies game-specific maze modifications.
    - Purpose: Keeps Pac-Man rules separate from the Grid
      and maze-generation algorithms.
    """

    @staticmethod
    def open_corners(grid: Grid) -> None:
        """
        Open the four maze corners as corridors.

        Each corner is connected to its two adjacent cells inside
        the grid by removing the corresponding walls.
        """
        # Top-left
        top_left = grid.get_cell(0, 0)
        top_left_right = grid.get_cell(0, 1)
        top_left_down = grid.get_cell(1, 0)

        if top_left is not None and top_left_right is not None:
            grid.remove_wall_between(
                top_left,
                top_left_right,
                Direction.EAST,
            )

        if top_left is not None and top_left_down is not None:
            grid.remove_wall_between(
                top_left,
                top_left_down,
                Direction.SOUTH,
            )

        # Top-right
        top_right = grid.get_cell(0, grid.width - 1)
        top_right_left = grid.get_cell(0, grid.width - 2)
        top_right_down = grid.get_cell(1, grid.width - 1)

        if top_right is not None and top_right_left is not None:
            grid.remove_wall_between(
                top_right,
                top_right_left,
                Direction.WEST,
            )

        if top_right is not None and top_right_down is not None:
            grid.remove_wall_between(
                top_right,
                top_right_down,
                Direction.SOUTH,
            )

        # Bottom-left
        bottom_left = grid.get_cell(grid.height - 1, 0)
        bottom_left_right = grid.get_cell(grid.height - 1, 1)
        bottom_left_up = grid.get_cell(grid.height - 2, 0)

        if bottom_left is not None and bottom_left_right is not None:
            grid.remove_wall_between(
                bottom_left,
                bottom_left_right,
                Direction.EAST,
            )

        if bottom_left is not None and bottom_left_up is not None:
            grid.remove_wall_between(
                bottom_left,
                bottom_left_up,
                Direction.NORTH,
            )

        # Bottom-right
        bottom_right = grid.get_cell(
            grid.height - 1,
            grid.width - 1,
        )
        bottom_right_left = grid.get_cell(
            grid.height - 1,
            grid.width - 2,
        )
        bottom_right_up = grid.get_cell(
            grid.height - 2,
            grid.width - 1,
        )

        if (
            bottom_right is not None
            and bottom_right_left is not None
        ):
            grid.remove_wall_between(
                bottom_right,
                bottom_right_left,
                Direction.WEST,
            )

        if bottom_right is not None and bottom_right_up is not None:
            grid.remove_wall_between(
                bottom_right,
                bottom_right_up,
                Direction.NORTH,
            )