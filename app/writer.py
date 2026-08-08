"""
Maze output Writer Module.

Exports grid wall states into hexadecimal
representations and path solution strings.
"""

from mazegen import Grid


class MazeWriter:
    """
    serializes grid cell bitmasks to file format.

    [Design Pattern: Output Serializer / Controller Helper]
    - Role: File Serializer
    - Purpose: Converts bitwise integer wall representations into standardized
      hexadecimal character outputs required for evaluation deliverables.
    """

    @staticmethod
    def write(
        grid: Grid,
        file_path: str,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path_str: str,
    ) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            for row in grid.matrix:
                hex_row = "".join(
                    f"{cell.walls:X}"
                    for cell in row
                )
                file.write(f"{hex_row}\n")
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit_pos[0]},{exit_pos[1]}\n")
            file.write(f"{path_str}\n")
