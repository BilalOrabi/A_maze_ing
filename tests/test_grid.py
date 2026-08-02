"""Unit tests for Grid matrix context."""

import pytest
from mazegen.cell import Direction
from mazegen.grid import Grid


def test_grid_invalid_dimensions() -> None:
    """Ensure Grid raises ValueError for non-positive dimensions."""
    with pytest.raises(ValueError, match="Grid dimensions must be positive integers."):
        Grid(width=0, height=5)

    with pytest.raises(ValueError, match="Grid dimensions must be positive integers."):
        Grid(width=5, height=-1)


def test_grid_bounds_checking() -> None:
    """Test boundary validation logic for in-bounds and out-of-bounds coordinates."""
    grid = Grid(width=3, height=3)

    assert grid.in_bounds(0, 0) is True
    assert grid.in_bounds(2, 2) is True
    assert grid.in_bounds(-1, 0) is False
    assert grid.in_bounds(0, -1) is False
    assert grid.in_bounds(0, 3) is False
    assert grid.in_bounds(3, 0) is False


def test_grid_get_cell() -> None:
    """Verify get_cell returns Cell instance or None if out of bounds."""
    grid = Grid(width=2, height=2)

    cell = grid.get_cell(1, 1)
    assert cell is not None
    assert cell.row == 1 and cell.col == 1

    assert grid.get_cell(5, 5) is None
    assert grid.get_cell(-1, 0) is None


def test_grid_get_neighbors() -> None:
    """Test neighbor retrieval for corner and central cells."""
    grid = Grid(width=3, height=3)

    # Corner cell (0, 0) should have exactly 2 valid in-bounds neighbors (EAST, SOUTH)
    top_left_cell = grid.get_cell(0, 0)
    assert top_left_cell is not None
    neighbors_corner = grid.get_neighbors(top_left_cell)
    assert len(neighbors_corner) == 2

    # Center cell (1, 1) should have 4 valid neighbors (NORTH, EAST, SOUTH, WEST)
    center_cell = grid.get_cell(1, 1)
    assert center_cell is not None
    neighbors_center = grid.get_neighbors(center_cell)
    assert len(neighbors_center) == 4


def test_grid_remove_wall_between() -> None:
    """Verify removing walls mutually updates both cells."""
    grid = Grid(width=2, height=1)
    c1 = grid.get_cell(0, 0)
    c2 = grid.get_cell(0, 1)

    assert c1 is not None and c2 is not None

    # Remove wall going EAST from c1 to c2
    grid.remove_wall_between(c1, c2, Direction.EAST)

    assert c1.has_wall(Direction.EAST) is False
    assert c2.has_wall(Direction.WEST) is False  # Opposite wall automatically removed


def test_grid_get_unvisited_neighbors() -> None:
    """Verify filtering of visited vs unvisited adjacent cells."""
    grid = Grid(width=2, height=1)
    c1 = grid.get_cell(0, 0)
    c2 = grid.get_cell(0, 1)

    assert c1 is not None and c2 is not None

    # Initially c2 is unvisited
    unvisited = grid.get_unvisited_neighbors(c1)
    assert len(unvisited) == 1
    assert unvisited[0] == (c2, Direction.EAST)

    # Mark c2 visited
    c2.visited = True
    assert len(grid.get_unvisited_neighbors(c1)) == 0
