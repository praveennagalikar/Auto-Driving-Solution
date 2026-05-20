"""Simulation engine: runs commands step-by-step, detects collisions."""

from collections import defaultdict
from typing import Optional

from auto_driving.car import Car
from auto_driving.field import Field


class SimulationResult:
    """Holds outcome for each car after the simulation completes."""

    def __init__(self) -> None:
        self._results: dict[str, str] = {}

    def add(self, car_name: str, result: str) -> None:
        self._results[car_name] = result

    def get(self, car_name: str) -> Optional[str]:
        return self._results.get(car_name)

    def all_results(self) -> list[str]:
        return list(self._results.values())


class Simulator:
    """
    Runs all cars step-by-step.

    At each step:
      1. Process one command per car (in addition order), skip collided cars.
      2. After all cars have moved for that step, check for collisions.
      3. Mark collided cars; they stop processing further commands.
    """

    def __init__(self, field: Field, cars: list[Car]) -> None:
        self.field = field
        self.cars = cars

    def run(self) -> SimulationResult:
        result = SimulationResult()
        max_steps = max((len(c.commands) for c in self.cars), default=0)

        for step in range(1, max_steps + 1):
            # Apply one command per active car
            for car in self.cars:
                if car.collided:
                    continue
                if step - 1 >= len(car.commands):
                    continue  # No more commands; car stays put

                cmd = car.commands[step - 1]
                self._apply_command(car, cmd)

            # Detect collisions after all cars have moved this step
            self._detect_collisions(step)

        # Build results
        for car in self.cars:
            if car.collision_info:
                result.add(car.name, f"- {car.name}, {car.collision_info}")
            else:
                result.add(car.name, f"- {car.name}, ({car.x},{car.y}) {car.direction}")

        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _apply_command(self, car: Car, cmd: str) -> None:
        if cmd == "L":
            car.turn_left()
        elif cmd == "R":
            car.turn_right()
        elif cmd == "F":
            nx, ny = car.next_position()
            if self.field.is_within_bounds(nx, ny):
                car.x, car.y = nx, ny
            # Out-of-bounds: command silently ignored

    def _detect_collisions(self, step: int) -> None:
        """
        Group active cars by position; flag any position with 2+ cars.
        Cars that were already collided before this step are excluded from
        triggering new collisions but can still share a cell with others
        (they won't move anyway).
        """
        position_map: dict[tuple[int, int], list[Car]] = defaultdict(list)

        for car in self.cars:
            if not car.collided:
                position_map[car.position()].append(car)

        for pos, occupants in position_map.items():
            if len(occupants) >= 2:
                x, y = pos
                names = [c.name for c in occupants]
                for car in occupants:
                    others = [n for n in names if n != car.name]
                    other_str = " and ".join(others)
                    car.collision_info = (
                        f"collides with {other_str} at ({x},{y}) at step {step}"
                    )
                    car.collided = True
