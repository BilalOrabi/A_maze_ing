"""
Unit tests for BFSSolver pathfinding strategy.
"""

from mazegen import Cell, Grid, Direction
from mazegen import BFSSolver


def test_bfs_solver_simple_path() -> None:
    """
    Test that BFSSolver successfully finds a path
    in a controlled 2x2 grid.
    """
    grid = Grid(2, 2)
    solver = BFSSolver()

    cell_0_0 = grid.get_cell(0, 0)
    cell_0_1 = grid.get_cell(0, 1)

    assert cell_0_0 is not None
    assert cell_0_1 is not None

    grid.remove_wall_between(cell_0_0, cell_0_1, Direction.EAST)

    # Solve from (0,0) to (0,1)
    path = solver.solve(grid, (0, 0), (0, 1))

    assert len(path) == 2
    assert path[0] == cell_0_0
    assert path[1] == cell_0_1


def test_bfs_solver_out_of_bounds() -> None:
    """
    Test that solver gracefully handles
    out-of-bounds start or end coordinates.
    """
    grid = Grid(3, 3)
    solver = BFSSolver()

    # Out of bounds end coordinate
    path = solver.solve(grid, (0, 0), (5, 5))

    assert path == []


def test_bfs_solver_no_path() -> None:
    """
    Test that solver returns an empty
    list when all walls are closed (no path).
    """
    grid = Grid(2, 2)
    solver = BFSSolver()

    path = solver.solve(grid, (0, 0), (1, 1))

    assert path == []


def test_path_to_directions_conversion() -> None:
    """
    Test converting an ordered cell path to
    N, E, S, W cardinal directions.
    """
    path = [Cell(0, 0), Cell(1, 0), Cell(1, 1), Cell(0, 1)]
    directions_str = BFSSolver.path_to_directions(path)
    assert directions_str == "SEN"


def test_bfs_solver_start_cell_none() -> None:
    """
    Test solver behavior when
    start position is technically out of bounds.
    """
    grid = Grid(2, 2)
    solver = BFSSolver()
    path = solver.solve(grid, (-1, 0), (1, 1))
    assert path == []
