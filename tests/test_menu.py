"""
Unit tests for the Interactive Terminal Menu Component.
"""

import subprocess
from unittest.mock import MagicMock, patch
import pytest

from app.menu import InteractiveMenu
from mazegen import Grid


@pytest.fixture
def setup_menu() -> tuple[InteractiveMenu, Grid]:
    """Fixture to instantiate a clean menu and grid configuration framework."""
    grid = Grid(2, 2)
    menu = InteractiveMenu(grid, entry=(0, 0), exit_pos=(1, 1))
    return menu, grid


def test_menu_initial_states(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Menu should initialize with default operational flags active."""
    menu, _ = setup_menu
    assert menu.show_path is True
    assert menu.color_enabled is True
    assert menu.theme_index == 0
    assert menu.running is True


def test_clear_screen_posix(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should invoke 'clear' binary when operating on Linux/macOS environments."""
    menu, _ = setup_menu
    with patch("os.name", "posix"), patch("subprocess.run") as mock_run:
        menu._clear_screen()
        mock_run.assert_called_once_with(["clear"], check=True)


def test_clear_screen_nt(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should invoke 'cls' command sequence when operating on Windows environments."""
    menu, _ = setup_menu
    with patch("os.name", "nt"), patch("subprocess.run") as mock_run:
        menu._clear_screen()
        mock_run.assert_called_once_with(["cls"], check=True)


def test_clear_screen_error_fallback(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should swallow execution errors cleanly if system binaries are unavailable."""
    menu, _ = setup_menu
    with patch("subprocess.run", side_effect=subprocess.SubprocessError):
        # Execution should pass safely without raising exceptions out of block
        menu._clear_screen()


def test_get_choice_strip_input(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should read standard input options cleanly, stripping extra whitespace characters."""
    menu, _ = setup_menu
    with patch("builtins.input", return_value="  2  "):
        assert menu._get_choice() == "2"


def test_get_choice_keyboard_interrupt(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should safely default back to option '4' (Quit) if standard stream is broken."""
    menu, _ = setup_menu
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        assert menu._get_choice() == "4"


def test_print_instructions_colored(setup_menu: tuple[InteractiveMenu, Grid], capsys: pytest.CaptureFixture[str]) -> None:
    """Should display active theme name variations when color mode features are enabled."""
    menu, _ = setup_menu
    menu.color_enabled = True
    menu.theme_index = 0

    menu._print_instructions()
    captured = capsys.readouterr()
    assert "Active: Classic Arcade Green" in captured.out


def test_print_instructions_monochrome(setup_menu: tuple[InteractiveMenu, Grid], capsys: pytest.CaptureFixture[str]) -> None:
    """Should fall back to clear monochrome indicator strings if color tracking is toggled off."""
    menu, _ = setup_menu
    menu.color_enabled = False

    menu._print_instructions()
    captured = capsys.readouterr()
    assert "Active: Monochrome" in captured.out


def test_run_loop_state_routing(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Should cycle operational state matrices cleanly across sequentially simulated inputs."""
    menu, _ = setup_menu

    # Sequence:
    # 2 -> Toggle path off
    # 3 -> Cycle theme index to 1
    # 1 -> Regenerate code path loop execution
    # 9 -> Hit invalid input default branch safety fall-through
    # 4 -> Terminate execution runner loop cleanly
    simulated_choices = ["2", "3", "1", "9", "4"]

    with patch.object(menu, "_get_choice", side_effect=simulated_choices), \
         patch.object(menu, "_clear_screen"), \
         patch("mazegen.BFSSolver.solve", return_value=[]), \
         patch("mazegen.MazeGenerator.generate") as mock_generate:

        menu.run()

        assert menu.show_path is False       # Verifies '2' route logic handled
        assert menu.theme_index == 1        # Verifies '3' route logic handled
        mock_generate.assert_called_once()  # Verifies '1' route logic handled
        assert menu.running is False        # Verifies '4' route logic handled


def test_run_loop_enable_color_fallback(setup_menu: tuple[InteractiveMenu, Grid]) -> None:
    """Option 3 should forcefully reset color flags if executing from basic monochrome mode."""
    menu, _ = setup_menu
    menu.color_enabled = False
    menu.theme_index = 3

    simulated_choices = ["3", "4"]

    with patch.object(menu, "_get_choice", side_effect=simulated_choices), \
         patch.object(menu, "_clear_screen"), \
         patch("mazegen.BFSSolver.solve", return_value=[]):

        menu.run()

        assert menu.color_enabled is True
        assert menu.theme_index == 0


def test_run_regeneration_increments_seed(
    setup_menu: tuple[InteractiveMenu, Grid],
) -> None:
    """Regenerating a seeded maze should advance its seed."""
    menu, _ = setup_menu
    menu.seed = 42

    with patch.object(menu, "_get_choice", side_effect=["1", "4"]), \
         patch.object(menu, "_clear_screen"), \
         patch("mazegen.BFSSolver.solve", return_value=[]), \
         patch("mazegen.MazeGenerator.generate"):
        menu.run()

    assert menu.seed == 43
