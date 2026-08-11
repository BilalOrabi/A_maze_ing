"""
Grid Data Model Module.

Manages the 2D spatial arrangement of cells and coordinate relationships.
"""

from typing import Optional
from mazegen.cell import Cell, Direction


class Grid:
    """
    Encapsulates a 2D matrix of Cell objects.

    [Design Pattern: Model / Spatial Context in MVC & Strategy]
    - Role: Domain Model Container & Spatial Context
    - Purpose: Acts as an implicit graph structure. Provides boundary checking
    and neighbor lookup methods consumed by generation and solving strategies.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a grid matrix filled with enclosed Cell instances.

        :param width: Number of columns in the grid.
        :param height: Number of rows in the grid.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive integers.")
        self.width: int = width
        self.height: int = height
        self.matrix: list[list[Cell]] = [
            [Cell(row, col) for col in range(width)]
            for row in range(height)
        ]

    def in_bounds(self, row: int, col: int) -> bool:
        """
        Checks if a coordinate pair lies within grid dimensions.

        :param row: Row index to test.
        :param col: Column index to test.
        :return: True if coordinate is inside grid boundaries.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """
        Safely retrieves a Cell object at a specific coordinate.

        :param row: Row index.
        :param col: Column index.
        :return: Cell instance if within bounds, otherwise None.
        """
        if self.in_bounds(row, col):
            return self.matrix[row][col]
        return None

    def get_neighbors(
        self, current_cell: Cell
    ) -> list[tuple[Cell, Direction, Direction]]:
        """
        Finds all valid adjacent in-bounds cells and their connecting
        directions.

        :param current_cell: Target Cell instance to find neighbors for.
        :return: List of tuples formatted as:
            (Neighbor Cell, Current Cell Wall, Neighbor Cell Opposite Wall)
        """
        valid_neighbors: list[tuple[Cell, Direction, Direction]] = []

        directional_offsets = [
            (-1, 0, Direction.NORTH),
            (0, 1, Direction.EAST),
            (1, 0, Direction.SOUTH),
            (0, -1, Direction.WEST),
        ]

        for row_offset, col_offset, wall_direction in directional_offsets:
            neighbor_row = current_cell.row + row_offset
            neighbor_col = current_cell.col + col_offset

            neighbor_cell = self.get_cell(neighbor_row, neighbor_col)
            if neighbor_cell:
                opposite_wall_direction = wall_direction.opposite()
                valid_neighbors.append(
                    (neighbor_cell, wall_direction, opposite_wall_direction)
                )

        return valid_neighbors

    def remove_wall_between(
        self, current: Cell, neighbor: Cell, direction: Direction
    ) -> None:
        """
        Removes the wall between current cell and neighbor cell in
        the given direction.
        Automatically removes the corresponding opposite wall on the
        neighbor using Enum.opposite.
        """
        current.remove_wall(direction)
        neighbor.remove_wall(direction.opposite())

    def get_unvisited_neighbors(
        self, cell: Cell
    ) -> list[tuple[Cell, Direction]]:
        """
        Returns a list of tuples (neighbor_cell, Direction) for all unvisited
        and non-reserved neighbors adjacent to the given cell.
        """
        unvisited_neighbors: list[tuple[Cell, Direction]] = []

        for neighbor_cell, wall_direction, _ in self.get_neighbors(cell):
            if not neighbor_cell.visited and not neighbor_cell.is_reserved:
                unvisited_neighbors.append((neighbor_cell, wall_direction))

        return unvisited_neighbors

    def get_reachable_neighbors(
        self, row: int, col: int
    ) -> list[tuple[int, int]]:
        """
        Get valid neighbor coordinates connected
        through open passages (no wall).

        :param row: Current row index.
        :param col: Current column index.
        :return: List of (row, col) tuples for reachable adjacent cells.
        """
        reachable_neighbors: list[tuple[int, int]] = []
        current_cell = self.get_cell(row, col)
        if not current_cell:
            return reachable_neighbors

        # Map directions to their coordinate offsets and wall flags
        direction_checks = [
            (-1, 0, Direction.NORTH),
            (0, 1, Direction.EAST),
            (1, 0, Direction.SOUTH),
            (0, -1, Direction.WEST),
        ]

        for row_offset, column_offset, wall_direction in direction_checks:
            neighbor_row = row + row_offset
            neighbor_col = col + column_offset

            if self.in_bounds(neighbor_row, neighbor_col):
                if not current_cell.has_wall(wall_direction):
                    reachable_neighbors.append((neighbor_row, neighbor_col))

        return reachable_neighbors

    def reset_cells(self) -> None:
        """
        Resets the structural states of all cells back to default.

        Clears visited tracking flags and restores all four walls using bitwise
        OR flags for every non-reserved cell to
        prepare for a new generation cycle.
        """
        all_walls = (
            Direction.NORTH | Direction.EAST | Direction.SOUTH | Direction.WEST
        )

        for row in self.matrix:
            for cell in row:
                cell.visited = False
                if not cell.is_reserved:
                    cell.walls = all_walls
