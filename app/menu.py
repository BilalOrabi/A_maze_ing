"""
Interactive Terminal Menu Component.

[Design Pattern: View/Controller Interaction]
Handles the interactive user loop required by Chapter 5, processing numeric
inputs to manage maze states and cycle color palettes.
"""

import os
import subprocess
from typing import Optional
from app.renderer import TerminalRenderer
from mazegen import Grid, MazeGenerator, BFSSolver, PacmanModifier


class InteractiveMenu:
    """Manages the interactive loop, input handling, and view states."""

    def __init__(
        self,
        grid: Grid,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        perfect: bool = False,
        seed: Optional[int] = None
    ) -> None:
        self.grid = grid
        self.entry = entry
        self.exit_pos = exit_pos
        self.renderer = TerminalRenderer()
        self.perfect = perfect
        self.seed = seed

        # Interactive States
        self.show_path = True
        self.color_enabled = True
        # 0: Green, 1: Cyberpunk, 2: Deep Ocean, 3: Sunset
        self.theme_index = 0
        self.running = True

    def _clear_screen(self) -> None:
        """
        Clears the terminal screen cleanly across
        platforms using subprocess.
        """
        try:
            # For Windows systems
            if os.name == "nt":
                subprocess.run(["cls"], check=True)
            # For Linux and macOS (42 cluster environments)
            else:
                subprocess.run(["clear"], check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fallback in case subprocess environment lacks terminal binaries
            pass

    def _print_instructions(self) -> None:
        """Prints the exact numeric choice banner.

        The banner showcases the active theme name.
        """
        if self.color_enabled:
            theme_name = self.renderer.THEMES[
                self.theme_index % len(self.renderer.THEMES)
            ]["name"]
            active_theme = f"Active: {theme_name}"
        else:
            active_theme = "Active: Monochrome"

        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print(f"3. Rotate maze colors ({active_theme})")
        print("4. Quit")

    def _get_choice(self) -> str:
        """Reads the user's choice string and waits for Enter."""
        try:
            return input("Choice? (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            return "4"  # Default to quit on break signals

    def run(self) -> None:
        """Main interaction loop."""
        solver = BFSSolver()
        generator = MazeGenerator()

        while self.running:
            self._clear_screen()

            # 1. Calculate shortest path if toggled on
            path = (
                solver.solve(self.grid, self.entry, self.exit_pos)
                if self.show_path
                else []
            )

            # 2. Render the current maze state passing the targeted
            #    theme configuration
            self.renderer.render(
                self.grid,
                theme_index=self.theme_index,
                use_color=self.color_enabled,
                entry=self.entry,
                exit_pos=self.exit_pos,
                path=path,
            )

            # 3. Print the choice listing
            self._print_instructions()

            # 4. Route choice logic
            choice = self._get_choice()

            match choice:
                case "1":

                    if self.seed is not None:
                        self.seed += 1

                    self.grid.reset_cells()
                    generator.generate(
                        self.grid,
                        start_row=self.entry[0],
                        start_col=self.entry[1],
                        exit_row=self.exit_pos[0],
                        exit_col=self.exit_pos[1],
                        apply_42=True,
                        seed=self.seed
                    )
                    if not self.perfect:
                        PacmanModifier.open_corners(self.grid)
                        PacmanModifier.open_center(self.grid)
                        PacmanModifier.add_loops(self.grid)
                        PacmanModifier.reduce_dead_ends(self.grid)

                case "2":
                    self.show_path = not self.show_path

                case "3":
                    if not self.color_enabled:
                        # If color was completely off, re-enable it on theme 0
                        self.color_enabled = True
                        self.theme_index = 0
                    else:
                        # Cycle cleanly through the 4 choices:
                        # 0 -> 1 -> 2 -> 3 -> 0
                        self.theme_index = (
                            self.theme_index + 1
                        ) % len(self.renderer.THEMES)

                case "4":
                    self.running = False
                    print("\nExiting application. Goodbye!")

                case _:  # The wildcard case acts exactly like default
                    # Invalid inputs just refresh the loop smoothly without
                    # doing anything
                    pass
