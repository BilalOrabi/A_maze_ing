"""
Maze Generator Strategy Module.

Encapsulates maze generation algorithms using the Strategy Pattern.
"""

from abc import ABC, abstractmethod
import random
from typing import Optional

from mazegen.grid import Grid
from mazegen.cell import Cell
from mazegen.mask import PatternMask


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
        exit_row: Optional[int] = None,
        exit_col: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> None:
        """
        Mutates the provided Grid instance in-place to construct a maze.

        :param grid: Grid instance to generate walls for.
        :param start_row: Starting row coordinate for the generator.
        :param start_col: Starting column coordinate for the generator.
        :param exit_row: Exit row coordinate.
        :param exit_col: Exit column coordinate.
        :param seed: Optional random seed for reproducible generation.
        """
        ...


class MazeGenerator(BaseGenerator):
    """
    Concrete Strategy: Randomized Depth-First Search (Iterative
    Backtracker).

    Carves passages in the grid using an explicit stack to prevent
    hitting Python's maximum recursion limit on large grids.
    """

    def generate(
        self,
        grid: Grid,
        start_row: int = 0,
        start_col: int = 0,
        exit_row: Optional[int] = None,
        exit_col: Optional[int] = None,
        seed: Optional[int] = None,
        apply_42: bool = True,
    ) -> None:
        # Create a local random generator.
        # Using a local RNG keeps the global random state untouched.
        rng = random.Random(seed)

        # 1. Handle mask logic if requested
        if apply_42 and not PatternMask.apply_42_mask(grid):
            print(
                "Error: maze is too small (or too narrow) for the 42 "
                "pattern."
            )

        # 2. Grab and validate the initial starting cell
        start_cell: Optional[Cell] = grid.get_cell(
            start_row,
            start_col,
        )

        if start_cell is None:
            raise ValueError(
                f"Start cell ({start_row}, {start_col}) is out of grid bounds."
            )

        # 3. Validate the exit only when it is provided
        if exit_row is not None and exit_col is not None:
            exit_cell: Optional[Cell] = grid.get_cell(
                exit_row,
                exit_col,
            )

            if exit_cell is None:
                raise ValueError(
                    f"exit cell ({exit_row}, {exit_col}) is out of grid bounds"
                )

            if (start_row, start_col) == (exit_row, exit_col):
                raise ValueError(
                    "ENTRY and EXIT must be different."
                )

        elif exit_row is not None or exit_col is not None:
            raise ValueError(
                "exit_row and exit_col must be provided together."
            )

        # 4. Handle conflict if ENTRY lands on the solid "42" pattern
        if start_cell.is_reserved:
            raise ValueError(
                "Configuration Error: ENTRY coordinate cannot be inside "
                "the '42' pattern mask."
            )

        # 5. Initialize generation stack
        start_cell.visited = True
        stack: list[Cell] = [start_cell]

        # 6. Iterative Backtracking Loop
        while stack:
            current_cell = stack[-1]
            unvisited_neighbors = grid.get_unvisited_neighbors(
                current_cell
            )

            if unvisited_neighbors:
                # Select a random unvisited neighbor
                # using the local seeded random generator.
                chosen_neighbor, direction = rng.choice(
                    unvisited_neighbors
                )

                # Carve wall between current and neighbor
                grid.remove_wall_between(
                    current_cell,
                    chosen_neighbor,
                    direction,
                )

                # Mark as visited and push to stack
                chosen_neighbor.visited = True
                stack.append(chosen_neighbor)

            else:
                # Dead end reached -> Backtrack
                stack.pop()
