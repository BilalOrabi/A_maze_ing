"""Tests for the terminal renderer."""

from _pytest.capture import CaptureFixture
from unittest.mock import patch

from app import TerminalRenderer
from mazegen import Grid, Cell, Direction


def test_renderer_outputs_maze(capsys: CaptureFixture[str]) -> None:
    """Renderer should print a valid ASCII maze."""
    grid = Grid(2, 2)

    renderer = TerminalRenderer()
    renderer.render(grid)

    captured = capsys.readouterr()
    output: str = captured.out

    assert "+---+---+" in output
    assert "|" in output


def test_renderer_skips_none_cell(capsys: CaptureFixture[str]) -> None:
    """Renderer should skip cells that are None."""
    grid = Grid(1, 1)
    renderer = TerminalRenderer()

    with patch.object(grid, "get_cell", return_value=None):
        renderer.render(grid)

    captured = capsys.readouterr()
    # If cell is skipped, content and walls aren't printed, leaving only the frame segments
    assert captured.out == "+---+\n|\n+\n"


def test_renderer_single_cell(capsys: CaptureFixture[str]) -> None:
    """Renderer should render a single cell."""
    grid = Grid(1, 1)

    renderer = TerminalRenderer()
    renderer.render(grid)

    captured = capsys.readouterr()
    expected = (
        "+---+\n"
        "|   |\n"
        "+---+\n"
    )

    assert captured.out == expected


def test_renderer_monochrome_elements(capsys: CaptureFixture[str]) -> None:
    """Renderer should print distinct symbols for entry, exit, path, and logo without colors."""
    grid = Grid(4, 1)
    
    # Setup state variations across cells
    cell_entry = grid.get_cell(0, 0)
    cell_exit = grid.get_cell(0, 1)
    cell_path = grid.get_cell(0, 2)
    cell_logo = grid.get_cell(0, 3)
    
    if cell_logo:
        cell_logo.is_reserved = True

    renderer = TerminalRenderer()
    renderer.render(
        grid=grid,
        use_color=False,
        entry=(0, 0),
        exit_pos=(0, 1),
        path=[cell_path] if cell_path else None
    )

    captured = capsys.readouterr()
    output = captured.out

    assert " E " in output
    assert " X " in output
    assert " ★ " in output
    assert "███" in output


def test_renderer_with_color_themes(capsys: CaptureFixture[str]) -> None:
    """Renderer should apply proper ANSI escape sequences based on the selected theme index."""
    grid = Grid(1, 1)
    cell = grid.get_cell(0, 0)
    if cell:
        cell.is_reserved = True

    renderer = TerminalRenderer()

    # Test Theme 0 (Classic Arcade Green) and Theme 1 (Cyberpunk Neon) via loop/modulo checks
    for theme_idx in [0, 1]:
        renderer.render(
            grid=grid,
            theme_index=theme_idx,
            use_color=True,
            entry=(0, 0),
            exit_pos=(0, 0),
            path=[cell] if cell else None
        )
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Ensure ANSI reset escape sequence is utilized when colors are active
        assert renderer.RESET in output
        assert renderer.BOLD in output


def test_renderer_open_passages(capsys: CaptureFixture[str]) -> None:
    """Renderer should render spaces instead of lines when walls are broken down."""
    grid = Grid(2, 2)
    
    cell_top_left = grid.get_cell(0, 0)
    cell_top_right = grid.get_cell(0, 1)
    cell_bottom_left = grid.get_cell(1, 0)

    # Knock down East wall and South wall to expose alternative string formatting branches
    if cell_top_left and cell_top_right and cell_bottom_left:
        grid.remove_wall_between(cell_top_left, cell_top_right, Direction.EAST)
        grid.remove_wall_between(cell_top_left, cell_bottom_left, Direction.SOUTH)

    renderer = TerminalRenderer()
    renderer.render(grid)

    captured = capsys.readouterr()
    output = captured.out

    # Checks that the structural divider walls are open spaces where expected
    assert "+   +" in output
