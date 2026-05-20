"""Input parsing and validation helpers."""

import re
from typing import Optional

VALID_DIRECTIONS = {"N", "S", "E", "W"}
VALID_COMMANDS = {"F", "L", "R"}


def parse_field_dimensions(raw: str) -> tuple[int, int]:
    """
    Parse 'width height' string.
    Raises ValueError on invalid input.
    """
    parts = raw.strip().split()
    if len(parts) != 2:
        raise ValueError("Please enter exactly two integers separated by a space.")
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError("Width and height must be integers.")
    if w <= 0 or h <= 0:
        raise ValueError("Width and height must be positive integers.")
    return w, h


def parse_initial_position(raw: str) -> tuple[int, int, str]:
    """
    Parse 'x y Direction' string.
    Raises ValueError on invalid input.
    """
    parts = raw.strip().split()
    if len(parts) != 3:
        raise ValueError("Please enter position in 'x y Direction' format.")
    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError("x and y must be integers.")
    direction = parts[2].upper()
    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"Direction must be one of: {', '.join(sorted(VALID_DIRECTIONS))}.")
    return x, y, direction


def parse_commands(raw: str) -> str:
    """
    Parse and validate a command string.
    Raises ValueError if unknown commands are present.
    """
    commands = raw.strip().upper()
    if not commands:
        raise ValueError("Command string cannot be empty.")
    invalid = set(commands) - VALID_COMMANDS
    if invalid:
        raise ValueError(
            f"Invalid command(s): {', '.join(sorted(invalid))}. "
            f"Only F, L, R are allowed."
        )
    return commands


def parse_car_name(raw: str) -> str:
    """
    Validate car name: non-empty, alphanumeric/underscore, no spaces.
    """
    name = raw.strip()
    if not name:
        raise ValueError("Car name cannot be empty.")
    if not re.match(r"^\w+$", name):
        raise ValueError("Car name must contain only letters, digits, or underscores.")
    return name
