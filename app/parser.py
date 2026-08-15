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
                    if int(value) <= 0:
                        raise ValueError(f"Invalid configuration line: {line}")
                    else:
                        config[key] = int(value)
                elif key in ("ENTRY", "EXIT"):
                    coords = [int(x) for x in value.split(",")]
                    if len(coords) != 2:
                        raise ValueError(
                            f"Invalid coordinate format for {key}: {value}"
                        )
                    config[key] = (coords[0], coords[1])
                elif key == "PERFECT":
                    if value.lower() == "true":
                        config[key] = True
                    elif value.lower() == "false":
                        config[key] = False
                    else:
                        raise ValueError(f"Invalid configuration line: {line}")

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
