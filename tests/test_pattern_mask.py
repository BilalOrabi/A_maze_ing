import pytest

from mazegen import Grid
from mazegen import PatternMask


class TestPatternMask:
    """Tests for the 42 pattern mask."""

    def test_can_fit_42_when_grid_is_large_enough(self) -> None:
        """42 should fit when the grid is at least the mask dimensions."""
        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        grid = Grid(mask_width, mask_height)

        assert PatternMask.can_fit_42(grid) is True

    def test_can_fit_42_when_grid_is_too_small(self) -> None:
        """42 should not fit when the grid is smaller than the mask."""
        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        grid = Grid(mask_width - 1, mask_height)

        assert PatternMask.can_fit_42(grid) is False

    def test_apply_42_mask_success(self) -> None:
        """Applying the mask should reserve the correct cells."""
        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        grid = Grid(mask_width, mask_height)

        result = PatternMask.apply_42_mask(grid)

        assert result is True

        for row in range(mask_height):
            for col in range(mask_width):
                cell = grid.get_cell(row, col)

                assert cell is not None

                if PatternMask.MASK_42[row][col] == 1:
                    assert cell.is_reserved is True
                else:
                    assert cell.is_reserved is False

    def test_apply_42_mask_too_small(self) -> None:
        """Applying the mask should fail when the grid is too small."""
        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        grid = Grid(mask_width - 1, mask_height)

        result = PatternMask.apply_42_mask(grid)

        assert result is False

    def test_42_cells_remain_fully_closed(self) -> None:
        """Reserved 42 cells should keep all four walls closed."""
        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        grid = Grid(mask_width, mask_height)

        PatternMask.apply_42_mask(grid)

        for row in range(mask_height):
            for col in range(mask_width):
                if PatternMask.MASK_42[row][col] == 1:
                    cell = grid.get_cell(row, col)

                    assert cell is not None
                    assert cell.walls == 15

    def test_42_is_centered(self) -> None:
        """The mask should be positioned in the center of a larger grid."""
        grid = Grid(20, 15)

        PatternMask.apply_42_mask(grid)

        mask_height = len(PatternMask.MASK_42)
        mask_width = len(PatternMask.MASK_42[0])

        start_row = (grid.height - mask_height) // 2
        start_col = (grid.width - mask_width) // 2

        for mask_row in range(mask_height):
            for mask_col in range(mask_width):
                grid_row = start_row + mask_row
                grid_col = start_col + mask_col

                cell = grid.get_cell(grid_row, grid_col)

                assert cell is not None

                if PatternMask.MASK_42[mask_row][mask_col] == 1:
                    assert cell.is_reserved is True