"""Unit tests for MazeGenerator strategy."""

import pytest
from mazegen.generator import BaseGenerator, MazeGenerator
from mazegen.grid import Grid


def test_abstract_base_generator() -> None:
    """Ensure BaseGenerator cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseGenerator()  # type: ignore[abstract]


@pytest.mark.parametrize(
    "start_row, start_col",
    [
        (5, 5),    # Beyond positive bounds
        (-1, 0),   # Negative row
        (0, -1),   # Negative col
    ],
)
def test_generator_invalid_start_coordinates(start_row: int, start_col: int) -> None:
    """Ensure generator raises ValueError for any out-of-bounds start coordinates."""
    grid = Grid(width=3, height=3)
    generator = MazeGenerator()

    with pytest.raises(ValueError, match="is out of grid bounds"):
        generator.generate(grid, start_row=start_row, start_col=start_col)


def test_generator_single_cell_grid() -> None:
    """Verify edge case behavior on a 1x1 grid."""
    grid = Grid(width=1, height=1)
    generator = MazeGenerator()

    generator.generate(grid, start_row=0, start_col=0)

    cell = grid.get_cell(0, 0)
    assert cell is not None
    assert cell.visited is True
    assert cell.walls == 15  # No neighbors to carve into


def test_generator_full_maze_traversal_and_spanning_tree() -> None:
    """
    Verify generator visits 100% of cells, carves walls, and satisfies
    spanning tree properties (carves exactly N - 1 passages).
    """
    width, height = 5, 5
    total_cells = width * height
    grid = Grid(width=width, height=height)
    generator = MazeGenerator()

    generator.generate(grid, start_row=0, start_col=0)

    visited_count = 0
    total_carved_walls = 0

    for r in range(height):
        for c in range(width):
            cell = grid.get_cell(r, c)
            assert cell is not None

            if cell.visited:
                visited_count += 1

            assert cell.walls < 15

            # Count missing walls for this cell
            # Bitwise 15 (1111) minus current bitmask gives missing walls count
            for wall_flag in (1, 2, 4, 8):
                if not cell.has_wall(wall_flag):
                    total_carved_walls += 1

    # 1. 100% traversal check
    assert visited_count == total_cells

    # 2. Spanning tree check: Each carved passage removes 2 cell walls.
    # Total carved cell walls must equal 2 * (N - 1)
    expected_carved_cell_walls = 2 * (total_cells - 1)
    assert total_carved_walls == expected_carved_cell_walls

def test_generator_invalid_exit_coordinates() -> None:
    """Generator should reject an exit outside the grid."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    with pytest.raises(ValueError, match="exit cell"):
        generator.generate(
            grid,
            start_row=0,
            start_col=0,
            exit_row=10,
            exit_col=10,
            apply_42=False,
        )


def test_generator_same_entry_and_exit() -> None:
    """Generator should reject identical entry and exit coordinates."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    with pytest.raises(
        ValueError,
        match="ENTRY and EXIT must be different",
    ):
        generator.generate(
            grid,
            start_row=0,
            start_col=0,
            exit_row=0,
            exit_col=0,
            apply_42=False,
        )


def test_generator_only_exit_row_provided() -> None:
    """Generator should require both exit coordinates together."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    with pytest.raises(
        ValueError,
        match="must be provided together",
    ):
        generator.generate(
            grid,
            start_row=0,
            start_col=0,
            exit_row=2,
            apply_42=False,
        )


def test_generator_only_exit_col_provided() -> None:
    """Generator should require both exit coordinates together."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    with pytest.raises(
        ValueError,
        match="must be provided together",
    ):
        generator.generate(
            grid,
            start_row=0,
            start_col=0,
            exit_col=2,
            apply_42=False,
        )


def test_generator_invalid_start_coordinates() -> None:
    """Generator should reject a start outside the grid."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    with pytest.raises(ValueError, match="Start cell"):
        generator.generate(
            grid,
            start_row=10,
            start_col=10,
            apply_42=False,
        )

def test_generator_rejects_reserved_entry() -> None:
    """Generator should reject an entry inside the 42 pattern."""
    grid = Grid(width=5, height=5)
    generator = MazeGenerator()

    cell = grid.get_cell(0, 0)
    assert cell is not None

    cell.is_reserved = True

    with pytest.raises(
        ValueError,
        match="ENTRY coordinate cannot be inside",
    ):
        generator.generate(
            grid,
            start_row=0,
            start_col=0,
            apply_42=False,
        )