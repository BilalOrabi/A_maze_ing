"""Unit tests for Cell model and Direction enum."""

from mazegen.cell import Cell, Direction


def test_direction_enum_values() -> None:
    """Verify Direction bitwise powers of 2."""
    assert Direction.NORTH == 1
    assert Direction.EAST == 2
    assert Direction.SOUTH == 4
    assert Direction.WEST == 8


def test_direction_opposite() -> None:
    """Verify opposite direction mappings for all cardinal points."""
    assert Direction.NORTH.opposite() == Direction.SOUTH
    assert Direction.SOUTH.opposite() == Direction.NORTH
    assert Direction.EAST.opposite() == Direction.WEST
    assert Direction.WEST.opposite() == Direction.EAST


def test_cell_initialization() -> None:
    """Verify default cell states and bitmask (all 4 walls set = 15)."""
    cell = Cell(row=2, col=3)
    assert cell.row == 2
    assert cell.col == 3
    assert cell.walls == 15  # 1 | 2 | 4 | 8
    assert cell.visited is False
    assert cell.is_reserved is False


def test_cell_wall_operations() -> None:
    """Verify wall presence checking and bitwise removal."""
    cell = Cell(row=0, col=0)

    # Initial check: all walls exist
    assert cell.has_wall(Direction.NORTH) is True
    assert cell.has_wall(Direction.EAST) is True
    assert cell.has_wall(Direction.SOUTH) is True
    assert cell.has_wall(Direction.WEST) is True

    # Remove NORTH wall (15 & ~1 = 14)
    cell.remove_wall(Direction.NORTH)
    assert cell.has_wall(Direction.NORTH) is False
    assert cell.has_wall(Direction.EAST) is True
    assert cell.walls == 14

    # Remove WEST wall (14 & ~8 = 6)
    cell.remove_wall(Direction.WEST)
    assert cell.has_wall(Direction.WEST) is False
    assert cell.walls == 6
