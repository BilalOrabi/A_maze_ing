"""
Maze Solver Strategy Module.

[Design Pattern: Strategy]
Provides a common interface for maze-solving algorithms and
implements Breadth-First Search (BFS).
"""

from abc import ABC, abstractmethod
from collections import deque

from mazegen import Cell, Grid

Coordinate = tuple[int, int]
Path = list[Cell]


class BaseSolver(ABC):
    """Abstract strategy interface for maze-solving algorithms."""

    @abstractmethod
    def solve(
        self,
        grid: Grid,
        start: Coordinate,
        end: Coordinate,
    ) -> Path:
        """
        Find a path through the grid from start to end.

        Args:
            grid: Populated Grid instance containing the maze.
            start: (row, column) coordinates of the entry point.
            end: (row, column) coordinates of the exit point.

        Returns:
            Ordered list of Cell instances from start to end.
            Returns an empty list if no path exists.
        """
        ...


class BFSSolver(BaseSolver):
    """Breadth-First Search solver implementation."""

    def solve(
        self,
        grid: Grid,
        start: Coordinate,
        end: Coordinate,
    ) -> Path:
        """
        Find the shortest path from start to end using BFS.

        BFS explores cells level by level. Since every movement between
        adjacent cells has the same cost, the first path found is the
        shortest path.
        """
        # Make sure both coordinates are inside the grid.
        if not grid.in_bounds(*start) or not grid.in_bounds(*end):
            return []

        start_cell = grid.get_cell(*start)

        if start_cell is None:
            return []

        # The queue stores the current position and the path
        # used to reach that position.
        queue: deque[tuple[Coordinate, Path]] = deque(
            [(start, [start_cell])]
        )

        # Keep track of cells that have already been discovered.
        visited: set[Coordinate] = {start}

        while queue:
            current_pos, path = queue.popleft()

            # We reached the destination.
            if current_pos == end:
                return path

            row, col = current_pos

            # Get only neighbors connected through open passages.
            for neighbor_row, neighbor_col in grid.get_reachable_neighbors(
                row,
                col,
            ):
                neighbor_pos = (neighbor_row, neighbor_col)

                # Skip cells that have already been discovered.
                if neighbor_pos in visited:
                    continue

                visited.add(neighbor_pos)

                neighbor_cell = grid.get_cell(
                    neighbor_row,
                    neighbor_col,
                )

                if neighbor_cell is None:
                    continue

                new_path = [*path, neighbor_cell]

                queue.append((neighbor_pos, new_path))

        # No path exists between start and end.
        return []

    @staticmethod
    def path_to_directions(path: Path) -> str:
        """
        Converts an ordered list of Cell instances into a continuous string
        of cardinal direction letters (N, E, S, W).

        Args:
            path: Ordered list of Cell instances from start to end.

        Returns:
            String representation of moves (e.g., "SWSESW...").
        """
        directions: list[str] = []

        for index in range(len(path) - 1):
            current_cell = path[index]
            next_cell = path[index + 1]

            row_difference = next_cell.row - current_cell.row
            col_difference = next_cell.col - current_cell.col

            if row_difference == -1 and col_difference == 0:
                directions.append("N")
            elif row_difference == 1 and col_difference == 0:
                directions.append("S")
            elif row_difference == 0 and col_difference == 1:
                directions.append("E")
            elif row_difference == 0 and col_difference == -1:
                directions.append("W")

        return "".join(directions)
