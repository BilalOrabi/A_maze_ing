"""
Cell Data Model Module.

Provides bitwise wall representation and cell state tracking for grid mazes.
"""

from enum import IntEnum


class Direction(IntEnum):
    """
    Bitwise representation of wall directions.

    Uses powers of 2 so directions can be combined or checked via bitwise ops.
    - NORTH: 1 (0001)
    - EAST:  2 (0010)
    - SOUTH: 4 (0100)
    - WEST:  8 (1000)
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def opposite(self) -> "Direction":
        """
        Returns the opposite direction flag for wall removal between neighbors.

        :return: Corresponding opposite Direction enum member.
        """
        opposite_mapping = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposite_mapping[self]


class Cell:
    """
    Represents a single discrete cell within a 2D maze grid.

    [Design Pattern: Model Component in MVC]
    - Role: Core Domain Data Model
    - Purpose: Encapsulates wall states using bitwise integers and tracks
      visitation states without any UI/rendering logic.
    """

    def __init__(self, row: int, col: int) -> None:
        """
        Initialize a cell with all four walls present by default (15 or 0xF).

        :param row: Row index in the grid matrix.
        :param col: Column index in the grid matrix.
        """
        self.row: int = row
        self.col: int = col
        # All 4 walls active by default: 1 | 2 | 4 | 8 = 15 (0xF)
        self.walls: int = (
            Direction.NORTH | Direction.EAST | Direction.SOUTH | Direction.WEST
        )
        self.visited: bool = False
        self.is_reserved: bool = False  # Reserved area (e.g., '42' pattern)

    def remove_wall(self, direction: Direction) -> None:
        """
        Knocks down a wall bit mask using bitwise AND with bitwise NOT (~).

        :param direction: The Direction enum flag to remove.
        """
        self.walls &= ~direction

    def has_wall(self, direction: Direction) -> bool:
        """
        Checks if a specific wall flag exists using bitwise AND.

        :param direction: The Direction enum flag to check.
        :return: True if the wall exists, False otherwise.
        """
        return bool(self.walls & direction)
