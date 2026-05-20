"""
CLI entry point for the Auto Driving Car Simulation.

Run with:
    python -m auto_driving
or (after `pip install -e .`):
    auto-driving
"""

import sys

from auto_driving.car import Car
from auto_driving.field import Field
from auto_driving.simulation import Simulator
from auto_driving.validators import (
    parse_car_name,
    parse_commands,
    parse_field_dimensions,
    parse_initial_position,
)


# ---------------------------------------------------------------------------
# I/O helpers — isolated for easy unit-testing / mocking
# ---------------------------------------------------------------------------

def _prompt(msg: str = "") -> str:
    """Print msg and return stripped user input. Raises EOFError on EOF."""
    if msg:
        print(msg)
    return input().strip()


def _print(msg: str = "") -> None:
    print(msg)


# ---------------------------------------------------------------------------
# Sub-flows
# ---------------------------------------------------------------------------

def _setup_field() -> Field:
    while True:
        try:
            raw = _prompt("Please enter the width and height of the simulation field in x y format:")
            w, h = parse_field_dimensions(raw)
            field = Field(w, h)
            _print(f"\nYou have created a field of {field}.")
            return field
        except ValueError as e:
            _print(f"Invalid input: {e} Please try again.")


def _add_car(field: Field, existing_names: set[str]) -> Car:
    # --- Name ---
    while True:
        try:
            raw = _prompt("\nPlease enter the name of the car:")
            name = parse_car_name(raw)
            if name in existing_names:
                _print(f"A car named '{name}' already exists. Please choose a different name.")
                continue
            break
        except ValueError as e:
            _print(f"Invalid input: {e} Please try again.")

    # --- Position ---
    while True:
        try:
            raw = _prompt(f"\nPlease enter initial position of car {name} in x y Direction format:")
            x, y, direction = parse_initial_position(raw)
            if not field.is_within_bounds(x, y):
                _print(
                    f"Position ({x},{y}) is outside the field ({field}). Please try again."
                )
                continue
            break
        except ValueError as e:
            _print(f"Invalid input: {e} Please try again.")

    # --- Commands ---
    while True:
        try:
            raw = _prompt(f"\nPlease enter the commands for car {name}:")
            commands = parse_commands(raw)
            break
        except ValueError as e:
            _print(f"Invalid input: {e} Please try again.")

    return Car(name=name, x=x, y=y, direction=direction, commands=commands)


def _print_car_list(cars: list[Car]) -> None:
    _print("\nYour current list of cars are:")
    for car in cars:
        _print(str(car))


def _print_menu_add_run() -> str:
    _print("\nPlease choose from the following options:")
    _print("[1] Add a car to field")
    _print("[2] Run simulation")
    return _prompt()


def _print_menu_restart_exit() -> str:
    _print("\nPlease choose from the following options:")
    _print("[1] Start over")
    _print("[2] Exit")
    return _prompt()


# ---------------------------------------------------------------------------
# Main simulation loop
# ---------------------------------------------------------------------------

def run_simulation_session() -> bool:
    """
    Run one full simulation session.
    Returns True if the user wants to start over, False to exit.
    """
    _print("\nWelcome to Auto Driving Car Simulation!\n")

    field = _setup_field()
    cars: list[Car] = []

    # --- Collect cars ---
    while True:
        _print_car_list(cars) if cars else None
        choice = _print_menu_add_run()

        if choice == "1":
            existing_names = {c.name for c in cars}
            car = _add_car(field, existing_names)
            cars.append(car)
            _print_car_list(cars)

        elif choice == "2":
            if not cars:
                _print("No cars added yet. Please add at least one car.")
                continue
            break

        else:
            _print("Invalid option. Please enter 1 or 2.")

    # --- Run ---
    _print_car_list(cars)

    simulator = Simulator(field, cars)
    result = simulator.run()

    _print("\nAfter simulation, the result is:")
    for line in result.all_results():
        _print(line)

    # --- Post-simulation ---
    while True:
        choice = _print_menu_restart_exit()
        if choice == "1":
            return True   # start over
        elif choice == "2":
            return False  # exit
        else:
            _print("Invalid option. Please enter 1 or 2.")


def main() -> None:
    try:
        while True:
            restart = run_simulation_session()
            if not restart:
                break
    except (EOFError, KeyboardInterrupt):
        pass  # graceful exit on Ctrl+C or piped input end

    _print("\nThank you for running the simulation. Goodbye!")


if __name__ == "__main__":
    main()
