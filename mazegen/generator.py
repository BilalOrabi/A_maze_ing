"""
Maze Generator Strategy Module.

Encapsulates maze generation algorithms using the Strategy Pattern.
"""

from abc import ABC, abstractmethod
import random
from mazegen import Grid
from mazegen import Cell


class BaseGenerator(ABC):
    """
    Abstract Strategy Interface for Maze Generators.

    [Design Pattern: Strategy Pattern]
    Defines the contract for all maze generation algorithms (e.g., DFS,
    Prim's).
    """

    @abstractmethod
    def generate(
        self,
        grid: Grid,
        start_row: int = 0,
        start_col: int = 0,
    ) -> None:
        """
        Mutates the provided Grid instance in-place to construct a maze.

        :param grid: Grid instance to generate walls for.
        :param start_row: Starting row coordinate for the generator
            algorithm.
        :param start_col: Starting column coordinate for the generator
            algorithm.
        """
        ...


class MazeGenerator(BaseGenerator):
    """
    Concrete Strategy: Randomized Depth-First Search (Iterative Backtracker).

    Carves passages in the grid using an explicit stack to prevent
    hitting Python's maximum recursion limit on large grids.
    """

    def generate(
        self,
        grid: Grid,
        start_row: int = 0,
        start_col: int = 0,
    ) -> None:
        start_cell = grid.get_cell(start_row, start_col)
        if start_cell is None:
            raise ValueError(
                f"Start cell ({start_row}, {start_col}) is out of grid bounds."
            )

        start_cell.visited = True
        stack: list[Cell] = [start_cell]

        while stack:
            current_cell = stack[-1]  # Peek at top of stack
            unvisited_neighbors = grid.get_unvisited_neighbors(current_cell)

            if unvisited_neighbors:
                # 1. Select a random unvisited neighbor
                chosen_neighbor, direction = random.choice(
                    unvisited_neighbors
                )

                # 2. Carve wall between current and neighbor
                grid.remove_wall_between(
                    current_cell,
                    chosen_neighbor,
                    direction,
                )

                # 3. Mark as visited and push to stack
                chosen_neighbor.visited = True
                stack.append(chosen_neighbor)
            else:
                # Dead end reached -> Backtrack
                stack.pop()
