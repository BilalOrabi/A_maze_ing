
"""Tests for the terminal renderer."""

from _pytest.capture import CaptureFixture

from app import TerminalRenderer
from mazegen import Grid


def test_renderer_outputs_maze(capsys: CaptureFixture[str]) -> None:
    """Renderer should print a valid ASCII maze."""

    grid = Grid(2, 2)

    renderer = TerminalRenderer()
    renderer.render(grid)

    captured = capsys.readouterr()

    output: str = captured.out

    assert "+---+---+" in output
    assert "|" in output


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
