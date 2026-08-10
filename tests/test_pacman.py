from mazegen import Direction, Grid
from mazegen import PacmanModifier


def test_open_corners() -> None:
    """All four corners should be connected to their two neighbors."""
    grid = Grid(5, 5)

    PacmanModifier.open_corners(grid)

    # Top-left
    top_left = grid.get_cell(0, 0)
    top_left_right = grid.get_cell(0, 1)
    top_left_down = grid.get_cell(1, 0)

    assert top_left is not None
    assert top_left_right is not None
    assert top_left_down is not None

    assert not top_left.has_wall(Direction.EAST)
    assert not top_left.has_wall(Direction.SOUTH)

    assert not top_left_right.has_wall(Direction.WEST)
    assert not top_left_down.has_wall(Direction.NORTH)

    # Top-right
    top_right = grid.get_cell(0, 4)
    top_right_left = grid.get_cell(0, 3)
    top_right_down = grid.get_cell(1, 4)

    assert top_right is not None
    assert top_right_left is not None
    assert top_right_down is not None

    assert not top_right.has_wall(Direction.WEST)
    assert not top_right.has_wall(Direction.SOUTH)

    assert not top_right_left.has_wall(Direction.EAST)
    assert not top_right_down.has_wall(Direction.NORTH)

    # Bottom-left
    bottom_left = grid.get_cell(4, 0)
    bottom_left_right = grid.get_cell(4, 1)
    bottom_left_up = grid.get_cell(3, 0)

    assert bottom_left is not None
    assert bottom_left_right is not None
    assert bottom_left_up is not None

    assert not bottom_left.has_wall(Direction.EAST)
    assert not bottom_left.has_wall(Direction.NORTH)

    assert not bottom_left_right.has_wall(Direction.WEST)
    assert not bottom_left_up.has_wall(Direction.SOUTH)

    # Bottom-right
    bottom_right = grid.get_cell(4, 4)
    bottom_right_left = grid.get_cell(4, 3)
    bottom_right_up = grid.get_cell(3, 4)

    assert bottom_right is not None
    assert bottom_right_left is not None
    assert bottom_right_up is not None

    assert not bottom_right.has_wall(Direction.WEST)
    assert not bottom_right.has_wall(Direction.NORTH)

    assert not bottom_right_left.has_wall(Direction.EAST)
    assert not bottom_right_up.has_wall(Direction.SOUTH)