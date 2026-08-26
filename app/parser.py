"""
Configuration parser Module.

Parses text-based configuration files into typed Python primitives.
"""
from typing import Any


class ConfigParser:
    """
    Reads and parses configuration parameters from text files.

    [Design Pattern : Controller Component in MVC]
    - Role: Configuration Reader / Controller Helper
    - Purpose: Encapsulates file I/O operation and converts key-value text
      into typed python data objects without exposing domain model logic.
    """

    @staticmethod
    def parse(file_path: str) -> dict[str, Any]:
        """
        Parses a key-value text configuration file.

        :param file_path: path to the configuration file.
        :return: Dictionary mapping configuration keys to typed values.
        """
        config: dict[str, Any] = {}

        def _parse_dimension(value: str, line: str) -> int:
            dimension = int(value)
            if dimension <= 0:
                raise ValueError(f"Invalid configuration line: {line}")
            return dimension

        def _parse_coordinates(key: str, value: str) -> tuple[int, int]:
            coords = [int(x) for x in value.split(",")]
            if len(coords) != 2:
                raise ValueError(
                    f"Invalid coordinate format for {key}: {value}"
                )
            return coords[0], coords[1]

        def _parse_perfect(value: str, line: str) -> bool:
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
            raise ValueError(f"Invalid configuration line: {line}")

        def _parse_seed(value: str) -> int:
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Invalid SEED value: {value}")

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid configuration line: {line}")

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key in ("WIDTH", "HEIGHT"):
                    config[key] = _parse_dimension(value, line)
                elif key in ("ENTRY", "EXIT"):
                    config[key] = _parse_coordinates(key, value)
                elif key == "PERFECT":
                    config[key] = _parse_perfect(value, line)
                elif key == "SEED":
                    config[key] = _parse_seed(value)
                else:
                    config[key] = value

        required_keys = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        }

        missing = required_keys - config.keys()
        if missing:
            raise ValueError(
                f"Missing configuration keys: {', '.join(sorted(missing))}"
            )

        if (
            config["WIDTH"] == 2
            and config["HEIGHT"] == 2
            and config["PERFECT"] is False
        ):
            raise ValueError(
                "Cannot build a Pac-Man maze with dimensions 2x2: "
                "it would have only 1 independent route, but a Pac-Man "
                "maze requires at least 2 independent routes."
            )

        return config
