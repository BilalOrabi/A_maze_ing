"""
Configuration parser Module.

Parses text-based configuration files into typed Python primitives.
"""
from typing import Dict, Any, Tuple


class ConfigParser:
    """
    Reads and parses configuration parameters from text files.

    [Design Pattern : Controller Component in MVC]
    - Role: Configuration Reader / Controller Helper
    - Purpose: Encapsulates file I/O operation and converts key-value text
      into typed python data objects without exposing domain model logic.
    """
    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """
        Parses a key-value text configuration file.

        :param file_path: path to the configuration file.
        :return: Dictionary mapping configuration keys to typed values.
        """
        config: Dict[str, Any] = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid configuration line: {line}")
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key in ("WIDTH", "HEIGHT"):
                    config[key] = int(value)
                elif key in ("ENTRY", "EXIT"):
                    coords: Tuple[int, ...] = tuple(map(int, value.split(",")))
                    config[key] = coords
                elif key == "PERFECT":
                    config[key] = value.lower() == "true"
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
        return config
