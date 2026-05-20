"""Car model: position, direction, commands, collision state."""

from dataclasses import dataclass, field
from typing import Optional

DIRECTIONS = ["N", "E", "S", "W"]
DIRECTION_DELTAS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass
class Car:
    name: str
    x: int
    y: int
    direction: str
    commands: str

    # Runtime state (not part of construction)
    collided: bool = field(default=False, init=False)
    collision_info: Optional[str] = field(default=None, init=False)

    def turn_left(self) -> None:
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx - 1) % 4]

    def turn_right(self) -> None:
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx + 1) % 4]

    def next_position(self) -> tuple[int, int]:
        dx, dy = DIRECTION_DELTAS[self.direction]
        return self.x + dx, self.y + dy

    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def __str__(self) -> str:
        return f"- {self.name}, ({self.x},{self.y}) {self.direction}, {self.commands}"
