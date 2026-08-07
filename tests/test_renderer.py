import pytest

from app.renderer import TerminalRenderer
from mazegen.grid import Grid


def test_renderer_outputs_maze(capsys):
    """Renderer should print a valid ASCII maze."""

    grid = Grid(2, 2)

    renderer = TerminalRenderer()
    renderer.render(grid)

    captured = capsys.readouterr()

    output = captured.out

    assert "+---+---+" in output
    assert "|" in output


def test_renderer_single_cell(capsys):
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


def test_renderer_single_cell(capsys):
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
