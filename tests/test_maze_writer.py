from pathlib import Path

from mazegen import Grid
from app import MazeWriter


def test_write_maze(tmp_path: Path) -> None:
    """Test that MazeWriter creates the correct output file."""
    grid: Grid = Grid(2, 2)

    file_path: Path = tmp_path / "maze.txt"

    entry: tuple[int, int] = (0, 0)
    exit_pos: tuple[int, int] = (1, 1)
    path_str: str = "ES"

    MazeWriter.write(
        grid=grid,
        file_path=str(file_path),
        entry=entry,
        exit_pos=exit_pos,
        path_str=path_str,
    )

    content: str = file_path.read_text(encoding="utf-8")
    lines: list[str] = content.splitlines()

    assert len(lines) == 6
    assert lines[2] == ""
    assert lines[3] == "0,0"
    assert lines[4] == "1,1"


def test_write_hex_values(tmp_path: Path) -> None:
    """Test hexadecimal wall representation."""
    grid: Grid = Grid(2, 1)

    grid.get_cell(0, 0).walls = 10
    grid.get_cell(0, 1).walls = 3

    file_path: Path = tmp_path / "maze.txt"

    MazeWriter.write(
        grid=grid,
        file_path=str(file_path),
        entry=(0, 0),
        exit_pos=(1, 0),
        path_str="E",
    )

    content: str = file_path.read_text(encoding="utf-8")

    assert content == (
        "A3\n"
        "\n"
        "0,0\n"
        "1,0\n"
        "E\n"
    )


def test_write_path(tmp_path: Path) -> None:
    """Test that the solution path is written correctly."""
    grid: Grid = Grid(1, 1)

    file_path: Path = tmp_path / "maze.txt"

    entry: tuple[int, int] = (0, 0)
    exit_pos: tuple[int, int] = (0, 0)
    path_str: str = "NNEESSWW"

    MazeWriter.write(
        grid=grid,
        file_path=str(file_path),
        entry=entry,
        exit_pos=exit_pos,
        path_str=path_str,
    )

    content: str = file_path.read_text(encoding="utf-8")

    assert content.endswith(
        "0,0\n"
        "0,0\n"
        "NNEESSWW\n"
    )


def test_output_file_is_created(tmp_path: Path) -> None:
    """Test that the output file is created."""
    grid: Grid = Grid(1, 1)

    file_path: Path = tmp_path / "output.txt"

    MazeWriter.write(
        grid=grid,
        file_path=str(file_path),
        entry=(0, 0),
        exit_pos=(0, 0),
        path_str="",
    )

    assert file_path.exists()