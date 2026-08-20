"""Tests for the configuration parser."""

from pathlib import Path
from typing import Any, Dict

import pytest

from app import ConfigParser


def test_parse_valid_config(tmp_path: Path) -> None:
    """Test parsing a valid configuration file."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=14,19",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
            ]
        ),
        encoding="utf-8",
    )

    config: Dict[str, Any] = ConfigParser.parse(str(config_file))

    assert config["WIDTH"] == 20
    assert config["HEIGHT"] == 15
    assert config["ENTRY"] == (0, 0)
    assert config["EXIT"] == (14, 19)
    assert config["OUTPUT_FILE"] == "maze.txt"
    assert config["PERFECT"] is True


def test_invalid_coordinates_raises_error(tmp_path: Path) -> None:
    """Invalid coordinate format should raise ValueError."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """
WIDTH=20
HEIGHT=20
ENTRY=0,0,5
EXIT=19,19
OUTPUT_FILE=test.txt
PERFECT=True
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_ignore_comments_and_blank_lines(tmp_path: Path) -> None:
    """Comments and blank lines should be ignored."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """
# comment

WIDTH=5

HEIGHT=5

ENTRY=0,0
EXIT=4,4
OUTPUT_FILE=test.txt
PERFECT=False
""",
        encoding="utf-8",
    )

    config: Dict[str, Any] = ConfigParser.parse(str(config_file))

    assert config["WIDTH"] == 5
    assert config["PERFECT"] is False


def test_invalid_line_raises_error(tmp_path: Path) -> None:
    """Invalid configuration line should raise ValueError."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """
WIDTH=20
HEIGHT=20
INVALID LINE
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=test.txt
PERFECT=True
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_missing_required_key(tmp_path: Path) -> None:
    """Missing required keys should raise ValueError."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """
WIDTH=20
HEIGHT=20
ENTRY=0,0
OUTPUT_FILE=test.txt
PERFECT=True
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_file_not_found() -> None:
    """Reading a non-existing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        ConfigParser.parse("does_not_exist.txt")

def test_parse_seed(tmp_path: Path) -> None:
    """SEED should be parsed as an integer."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
                "SEED=42",
            ]
        ),
        encoding="utf-8",
    )

    config: Dict[str, Any] = ConfigParser.parse(str(config_file))

    assert config["SEED"] == 42
    assert isinstance(config["SEED"], int)


def test_invalid_width_raises_error(tmp_path: Path) -> None:
    """WIDTH must be greater than zero."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=0",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_invalid_height_raises_error(tmp_path: Path) -> None:
    """HEIGHT must be greater than zero."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=-1",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_invalid_perfect_raises_error(tmp_path: Path) -> None:
    """PERFECT must contain True or False."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=maybe",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))


def test_invalid_seed_raises_error(tmp_path: Path) -> None:
    """SEED must be an integer."""
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
                "SEED=abc",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ConfigParser.parse(str(config_file))