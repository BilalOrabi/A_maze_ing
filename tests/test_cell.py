from mazegen.cell import Cell, Direction


def test_cell_initialization() -> None:

    cell = Cell(0, 0)
    assert cell.walls == 15
    assert cell.visited is False


def test_remove_wall() -> None:
    cell = Cell(0, 0)
    cell.remove_wall(Direction.NORTH)
    assert cell.has_wall(Direction.NORTH) is False
    assert cell.has_wall(Direction.SOUTH) is True
    assert cell.walls == 14


def test_direction_opposite() -> None:
    assert Direction.NORTH.opposite() == Direction.SOUTH
    assert Direction.EAST.opposite() == Direction.WEST
