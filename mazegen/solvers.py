"""
Maze Solver Strategy Module.

[Design Pattern: Strategy]
Provides an abstract base class for pathfinding algorithms (e.g., BFS, A*).
"""

from abc import ABC, abstractmethod
from mazegen import Cell
from mazegen import Grid


class BaseSolver(ABC):
    """Abstract Strategy interface for maze-solving algorithms."""

    @abstractmethod
    def solve(
        self, grid: Grid, start: tuple[int, int], end: tuple[int, int]
    ) -> list[Cell]:
        """Find a path through the grid from start to end coordinates.

        :param grid: Populated Grid instance with carved passages.
        :param start: (row, col) coordinates for the entry point.
        :param end: (row, col) coordinates for the exit point.
        :return: Ordered list of Cell instances from start to end.
        """
        ...


class BFSSolver(BaseSolver):

    def solve(
            self, grid: Grid, start: tuple[int, int], end: tuple[int, int]
        ) -> list[Cell]:
        pass
