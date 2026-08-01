from mazegen.grid import Grid


def test_grid_in_bounds() -> None:
    grid = Grid(width=3, height=3)
    assert grid.in_bounds(0, 0) is True
    assert grid.in_bounds(2, 2) is True
    assert grid.in_bounds(-1, 0) is False
    assert grid.in_bounds(3, 3) is False
    assert grid.in_bounds(2, 3) is False
    assert grid.in_bounds(3, 2) is False


def test_get_neighbors_corner() -> None:
    grid = Grid(width=2, height=2)
    top_left_cell = grid.matrix[0][0]
    neighbors = grid.get_neighbors(top_left_cell)

    # Top-left corner (0,0) in a 2x2 grid
    # should only have 2 neighbors (EAST and SOUTH)
    assert len(neighbors) == 2

    # Verify return tuple contents: (neighbor_cell, wall, opposite_wall)
    neighbor_cells = [n[0] for n in neighbors]
    assert grid.matrix[0][1] in neighbor_cells  # EAST neighbor
    assert grid.matrix[1][0] in neighbor_cells  # SOUTH neighbor
