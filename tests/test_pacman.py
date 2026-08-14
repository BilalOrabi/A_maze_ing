from mazegen import Direction, Grid, MazeGenerator
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


def test_open_center_11x11() -> None:
    """Open a passage close to the center of an odd-sized grid."""
    grid = Grid(11, 11)

    PacmanModifier.open_center(grid)

    center_row = (grid.height - 1) / 2
    center_col = (grid.width - 1) / 2

    best_distance = float("inf")
    found_open_passage = False

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(row, col)

            assert cell is not None

            for neighbor, direction, _ in grid.get_neighbors(cell):
                if not cell.has_wall(direction):
                    pair_row = (cell.row + neighbor.row) / 2
                    pair_col = (cell.col + neighbor.col) / 2

                    distance = (
                        abs(pair_row - center_row)
                        + abs(pair_col - center_col)
                    )

                    if distance < best_distance:
                        best_distance = distance
                        found_open_passage = True

    assert found_open_passage is True
    assert best_distance <= 1.0


def test_open_center_12x12() -> None:
    """Open a passage close to the center of an even-sized grid."""
    grid = Grid(12, 12)

    PacmanModifier.open_center(grid)

    center_row = (grid.height - 1) / 2
    center_col = (grid.width - 1) / 2

    best_distance = float("inf")
    found_open_passage = False

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(row, col)

            assert cell is not None

            for neighbor, direction, _ in grid.get_neighbors(cell):
                if not cell.has_wall(direction):
                    pair_row = (cell.row + neighbor.row) / 2
                    pair_col = (cell.col + neighbor.col) / 2

                    distance = (
                        abs(pair_row - center_row)
                        + abs(pair_col - center_col)
                    )

                    if distance < best_distance:
                        best_distance = distance
                        found_open_passage = True

    assert found_open_passage is True
    assert best_distance <= 1.0


def test_open_center_does_not_modify_reserved_cells() -> None:
    """The center modification must never open a reserved 42 cell."""
    grid = Grid(20, 15)

    # Reserve a small area around the center.
    center_row = grid.height // 2
    center_col = grid.width // 2

    reserved_cells = [
        grid.get_cell(center_row, center_col),
        grid.get_cell(center_row, center_col + 1),
        grid.get_cell(center_row + 1, center_col),
    ]

    for cell in reserved_cells:
        assert cell is not None
        cell.is_reserved = True

    reserved_walls = {
        (cell.row, cell.col): cell.walls
        for cell in reserved_cells
        if cell is not None
    }

    PacmanModifier.open_center(grid)

    for cell in reserved_cells:
        assert cell is not None
        assert cell.walls == reserved_walls[(cell.row, cell.col)]


def test_open_center_creates_new_passage() -> None:
    """open_center should remove at least one wall."""
    grid = Grid(15, 15)

    initial_wall_count = sum(
        bin(cell.walls).count("1")
        for row in grid.matrix
        for cell in row
    )

    PacmanModifier.open_center(grid)

    final_wall_count = sum(
        bin(cell.walls).count("1")
        for row in grid.matrix
        for cell in row
    )

    assert final_wall_count < initial_wall_count

def count_walls(grid: Grid) -> int:
    """Count all walls in the grid."""
    return sum(
        bin(cell.walls).count("1")
        for row in grid.matrix
        for cell in row
    )


def test_add_loops() -> None:
    """Add at least two extra passages to the maze."""
    grid = Grid(10, 10)

    initial_walls = count_walls(grid)

    PacmanModifier.add_loops(grid)

    final_walls = count_walls(grid)

    # Every removed passage removes two walls:
    # one from each of the two connected cells.
    assert initial_walls - final_walls >= 4

def count_open_connections(grid: Grid) -> int:
    """Count unique open connections between adjacent cells."""
    connections = 0

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(row, col)

            assert cell is not None

            for neighbor, direction, _ in grid.get_neighbors(cell):
                # Count each connection only once.
                if (
                    neighbor.row < cell.row
                    or (
                        neighbor.row == cell.row
                        and neighbor.col <= cell.col
                    )
                ):
                    continue

                if not cell.has_wall(direction):
                    connections += 1

    return connections


def test_add_loops_after_dfs() -> None:
    """
    Verify that add_loops adds at least two new connections
    to a DFS-generated perfect maze.
    """
    grid = Grid(10, 10)

    generator = MazeGenerator()
    generator.generate(
        grid,
        start_row=0,
        start_col=0,
    )

    connections_before = count_open_connections(grid)

    PacmanModifier.add_loops(grid)

    connections_after = count_open_connections(grid)

    assert connections_after - connections_before >= 2

def test_open_center_skips_open_wall() -> None:
    """open_center should skip passages that are already open."""
    grid = Grid(5, 5)

    current = grid.get_cell(2, 2)
    neighbor = grid.get_cell(2, 3)

    assert current is not None
    assert neighbor is not None

    grid.remove_wall_between(
        current,
        neighbor,
        Direction.EAST,
    )

    PacmanModifier.open_center(grid)


def test_open_center_no_valid_pair() -> None:
    """open_center should handle a grid with no valid cells."""
    grid = Grid(5, 5)

    for row in grid.matrix:
        for cell in row:
            cell.is_reserved = True

    PacmanModifier.open_center(grid)


def test_add_loops_skips_reserved_current() -> None:
    """add_loops should skip reserved current cells."""
    grid = Grid(5, 5)

    for row in grid.matrix:
        for cell in row:
            cell.is_reserved = True

    PacmanModifier.add_loops(grid)


def test_add_loops_skips_reserved_neighbor() -> None:
    """add_loops should skip reserved neighbors."""
    grid = Grid(5, 5)

    current = grid.get_cell(2, 2)
    neighbor = grid.get_cell(2, 3)

    assert current is not None
    assert neighbor is not None

    neighbor.is_reserved = True

    PacmanModifier.add_loops(grid)

def test_count_open_neighbors_zero() -> None:
    """A fully enclosed cell has zero open neighbors."""
    grid = Grid(5, 5)
    cell = grid.get_cell(2, 2)

    assert cell is not None
    assert PacmanModifier.count_open_neighbors(grid, cell) == 0


def test_count_open_neighbors_one() -> None:
    """A cell with one open passage is a dead end."""
    grid = Grid(5, 5)

    cell = grid.get_cell(2, 2)
    neighbor = grid.get_cell(2, 3)

    assert cell is not None
    assert neighbor is not None

    grid.remove_wall_between(
        cell,
        neighbor,
        Direction.EAST,
    )

    assert PacmanModifier.count_open_neighbors(grid, cell) == 1


def test_count_open_neighbors_two() -> None:
    """A cell with two open passages is not a dead end."""
    grid = Grid(5, 5)

    cell = grid.get_cell(2, 2)
    east = grid.get_cell(2, 3)
    south = grid.get_cell(3, 2)

    assert cell is not None
    assert east is not None
    assert south is not None

    grid.remove_wall_between(
        cell,
        east,
        Direction.EAST,
    )

    grid.remove_wall_between(
        cell,
        south,
        Direction.SOUTH,
    )

    assert PacmanModifier.count_open_neighbors(grid, cell) == 2

def count_dead_ends(grid: Grid) -> int:
    """Count non-reserved cells with exactly one open passage."""
    count = 0

    for row in grid.matrix:
        for cell in row:
            if cell.is_reserved:
                continue

            if PacmanModifier.count_open_neighbors(grid, cell) == 1:
                count += 1

    return count


def test_reduce_dead_ends() -> None:
    """Reduce the number of dead ends in a generated maze."""
    grid = Grid(10, 10)

    generator = MazeGenerator()
    generator.generate(
        grid,
        start_row=0,
        start_col=0,
    )

    dead_ends_before = count_dead_ends(grid)

    PacmanModifier.reduce_dead_ends(grid)

    dead_ends_after = count_dead_ends(grid)

    assert dead_ends_after < dead_ends_before


def test_reduce_dead_ends_preserves_reserved_cells() -> None:
    """reduce_dead_ends must not modify reserved cells."""
    grid = Grid(10, 10)

    generator = MazeGenerator()
    generator.generate(
        grid,
        start_row=0,
        start_col=0,
    )

    reserved_cells = [
        grid.get_cell(4, 4),
        grid.get_cell(4, 5),
        grid.get_cell(5, 4),
        grid.get_cell(5, 5),
    ]

    for cell in reserved_cells:
        assert cell is not None
        cell.is_reserved = True

    walls_before = {
        (cell.row, cell.col): cell.walls
        for cell in reserved_cells
        if cell is not None
    }

    PacmanModifier.reduce_dead_ends(grid)

    for cell in reserved_cells:
        assert cell is not None
        assert cell.walls == walls_before[(cell.row, cell.col)]
