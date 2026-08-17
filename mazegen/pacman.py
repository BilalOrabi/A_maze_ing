"""
Pac-Man Maze Modifier.

Provides modifications required for PERFECT=False mazes.
"""

from mazegen import Direction, Grid, Cell


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

    @staticmethod
    def open_center(grid: Grid) -> None:
        """
        Create an open corridor as close as possible to the grid center.

        Reserved cells belonging to the 42 pattern are never modified.
        The closest pair of adjacent non-reserved cells is selected and
        the wall between them is removed.
        """
        # Determining the center of the grid
        center_row = (grid.height - 1) / 2
        center_col = (grid.width - 1) / 2
        # the best pair of cells we found stores
        best_pair: tuple[Cell, Cell, Direction] | None = None
        best_distance: float = float("inf")

        for row in range(grid.height):
            for col in range(grid.width):
                current = grid.get_cell(row, col)
                if current is None or current.is_reserved:
                    continue

                for neighbor, direction, _ in grid.get_neighbors(current):
                    if neighbor.is_reserved:
                        continue
                    # We only want to remove an existing wall.
                    if not current.has_wall(direction):
                        continue

                    if (
                        neighbor.row < current.row
                        or (
                            neighbor.row == current.row
                            and neighbor.col <= current.col
                        )
                    ):
                        continue
                    # Wall location calculation
                    pair_row = (current.row + neighbor.row) / 2
                    pair_col = (current.col + neighbor.col) / 2

                    distance = (
                        abs(pair_row - center_row)
                        + abs(pair_col - center_col)
                    )
                    if distance < best_distance:
                        best_distance = distance
                        best_pair = (
                            current,
                            neighbor,
                            direction,
                        )
        if best_pair is None:
            print("Error: unable to create center corridor.")
            return

        current, neighbor, direction = best_pair

        grid.remove_wall_between(
            current,
            neighbor,
            direction,
        )

    @staticmethod
    def add_loops(grid: Grid) -> None:
        """
        ِAdd extra passages to create loops in the maze.

        Only walls between two non-reserved adjacent cells are considered.
        At least two additional passages are created when enough candidates
        are available

        [Design Pattern: Modifier / Post-Processing Component]
        - Role: Applies Pac-Man maze modifications.
        - Purpose: Adds extra connections to a perfect maze, creating loops.
        """
        candidates: list[tuple[Cell, Cell, Direction]] = []

        for row in range(grid.height):
            for col in range(grid.width):
                current = grid.get_cell(row, col)

                if current is None or current.is_reserved:
                    continue

                for neighbor, direction, _ in grid.get_neighbors(current):
                    if neighbor.is_reserved:
                        continue

                    if (
                        neighbor.row < current.row
                        or (
                            neighbor.row == current.row
                            and neighbor.col <= current.col
                        )
                    ):
                        continue

                    if not current.has_wall(direction):
                        continue
                    candidates.append(
                        (current, neighbor, direction)
                    )

        loops_to_add = min(23, len(candidates))
        if loops_to_add == 0:
            return

        for i in range(loops_to_add):
            index = i * len(candidates) // loops_to_add
            current, neighbor, direction = candidates[index]
            grid.remove_wall_between(
                current,
                neighbor,
                direction,
            )

    @staticmethod
    def count_open_neighbors(grid: Grid, cell: Cell) -> int:
        """Count the number of open passages from a cell."""
        count = 0

        for neighbor, direction, _ in grid.get_neighbors(cell):
            if not cell.has_wall(direction):
                count += 1

        return count

    @staticmethod
    def reduce_dead_ends(grid: Grid) -> None:
        """
        Reduce the number of dead ends in the maze.

        Finds dead-end cells and opens one additional passage from
        selected dead ends. Reserved cells belonging to the 42 pattern
        are never modified.

        [Design Pattern: Modifier / Post-Processing Component]
        - Role: Applies Pac-Man maze nodifications.
        - purpose: Reduces excessive dead ends while preserving
          the overall maze structure
        """

        dead_ends: list[Cell] = []

        for row in range(grid.height):
            for col in range(grid.width):
                current = grid.get_cell(row, col)

                if current is None or current.is_reserved:
                    continue
                if PacmanModifier.count_open_neighbors(
                    grid,
                    current,
                ) == 1:
                    dead_ends.append(current)

        modify_dead_ends = len(dead_ends)

        for cell in dead_ends[:modify_dead_ends]:
            for neighbor, direction, _ in grid.get_neighbors(cell):
                if neighbor.is_reserved:
                    continue

                if not cell.has_wall(direction):
                    continue

                grid.remove_wall_between(
                    cell,
                    neighbor,
                    direction,
                )

                break
