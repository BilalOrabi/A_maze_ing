"""
Unit tests for BFSSolver pathfinding strategy.
"""

from unittest.mock import patch
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


def test_bfs_solver_start_cell_mock_none() -> None:
    """
    Test solver behavior when the start coordinate is inside bounds
    but its internal Cell object evaluates directly to None.
    """
    grid = Grid(2, 2)
    solver = BFSSolver()

    with patch.object(grid, "get_cell", return_value=None):
        path = solver.solve(grid, (0, 0), (1, 1))
        assert path == []


def test_bfs_solver_skips_visited_neighbors() -> None:
    """
    Test that the solver correctly skips looking at neighbors
    that have already been added to the visited tracking registry.
    """
    # Initialize a grid that explicitly has 3 columns and 1 row
    grid = Grid(width=3, height=1)
    solver = BFSSolver()

    cell_0_0 = grid.get_cell(0, 0)
    cell_0_1 = grid.get_cell(0, 1)
    cell_0_2 = grid.get_cell(0, 2)

    # If your Grid(rows, cols) uses the opposite layout order, 
    # let's fallback to a safe 3x3 grid to guarantee the cells exist:
    if cell_0_0 is None or cell_0_1 is None or cell_0_2 is None:
        grid = Grid(width=3, height=3)
        cell_0_0 = grid.get_cell(0, 0)
        cell_0_1 = grid.get_cell(0, 1)
        cell_0_2 = grid.get_cell(0, 2)

    assert cell_0_0 is not None
    assert cell_0_1 is not None
    assert cell_0_2 is not None

    # Carve a clear path line: (0,0) <-> (0,1) <-> (0,2)
    grid.remove_wall_between(cell_0_0, cell_0_1, Direction.EAST)
    grid.remove_wall_between(cell_0_1, cell_0_2, Direction.EAST)

    # Solving forces cell (0,1) to check its backwards step (0,0), triggering the hit
    path = solver.solve(grid, (0, 0), (0, 2))
    assert len(path) == 3


def test_bfs_solver_neighbor_is_none() -> None:
    """
    Test that the execution loops past and skips any neighbor coordinate
    that unexpectedly maps out to a None cell state during execution.
    """
    grid = Grid(2, 2)
    solver = BFSSolver()

    cell_0_0 = grid.get_cell(0, 0)
    cell_0_1 = grid.get_cell(0, 1)

    assert cell_0_0 is not None
    assert cell_0_1 is not None

    grid.remove_wall_between(cell_0_0, cell_0_1, Direction.EAST)

    original_get_cell = grid.get_cell

    # Keep the root node entry valid, but obscure neighbor lookup loops
    def mock_get_cell(row: int, col: int) -> Cell | None:
        if (row, col) == (0, 0):
            return original_get_cell(row, col)
        return None

    with patch.object(grid, "get_cell", side_effect=mock_get_cell):
        path = solver.solve(grid, (0, 0), (0, 1))
        assert path == []


def test_path_to_directions_west_fallback() -> None:
    """
    Test path_to_directions with alternative directional changes
    to fully exercise the West cardinal mapping branch and empty steps.
    """
    path = [Cell(1, 1), Cell(1, 0)]
    directions_str = BFSSolver.path_to_directions(path)
    assert directions_str == "W"

    # Test completely empty path execution boundaries
    assert BFSSolver.path_to_directions([]) == ""