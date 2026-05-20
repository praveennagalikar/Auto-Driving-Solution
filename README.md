# Auto Driving Car Simulation

A production-grade command-line simulation of autonomous vehicles navigating a rectangular field, with step-by-step command execution and multi-car collision detection.

---

## Features

- Define a rectangular simulation field of any size
- Add multiple cars, each with a unique name, starting position, and command sequence
- Commands: `F` (forward), `L` (rotate left 90°), `R` (rotate right 90°)
- Out-of-bounds commands are silently ignored — cars stay in place
- Multi-car simulation with step-by-step interleaving (one command per car per step)
- Collision detection: first step where two or more cars occupy the same cell
- Collided cars stop immediately and do not process further commands
- Post-simulation: start over or exit

---

## Requirements

- Python **3.10** or later (uses `tuple[int, int]` type hints)
- No third-party runtime dependencies

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/auto-driving.git
cd auto-driving

# (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# Install in editable mode (exposes the `auto-driving` CLI command)
pip install -e .
```

---

## Running the Simulation

```bash
# Option 1: via the installed CLI command
auto-driving

# Option 2: via the module
python -m auto_driving

# Option 3: directly
python src/auto_driving/main.py
```

### Example Session (Scenario 1 — single car)

```
Welcome to Auto Driving Car Simulation!

Please enter the width and height of the simulation field in x y format:
10 10

You have created a field of 10 x 10.

Please choose from the following options:
[1] Add a car to field
[2] Run simulation
1

Please enter the name of the car:
A

Please enter initial position of car A in x y Direction format:
1 2 N

Please enter the commands for car A:
FFRFFFFRRL

Your current list of cars are:
- A, (1,2) N, FFRFFFFRRL

Please choose from the following options:
[1] Add a car to field
[2] Run simulation
2

Your current list of cars are:
- A, (1,2) N, FFRFFFFRRL

After simulation, the result is:
- A, (5,4) S

Please choose from the following options:
[1] Start over
[2] Exit
2

Thank you for running the simulation. Goodbye!
```

### Example Session (Scenario 2 — collision)

```
...
After simulation, the result is:
- A, collides with B at (5,4) at step 7
- B, collides with A at (5,4) at step 7
```

---

## Running the Tests

```bash
# Install dev dependencies (pytest + coverage)
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=auto_driving --cov-report=term-missing

# Run a specific test file
pytest tests/test_simulation.py -v
```

### Expected Output

```
tests/test_car.py         ........ [ 8 tests]
tests/test_field.py       ........ [ 8 tests]
tests/test_validators.py  ............. [13 tests]
tests/test_simulation.py  .............. [14 tests]
tests/test_integration.py ............ [12 tests]

55 passed in <1s
```

---

## Project Structure

```
auto-driving/
├── src/
│   └── auto_driving/
│       ├── __init__.py        Package marker
│       ├── __main__.py        Enables `python -m auto_driving`
│       ├── car.py             Car dataclass (position, direction, commands)
│       ├── field.py           Field (dimensions, bounds checking)
│       ├── simulation.py      Simulator engine (BFS step execution, collision detection)
│       ├── validators.py      Input parsing & validation helpers
│       └── main.py            CLI entry point & user interaction loop
├── tests/
│   ├── conftest.py            pytest path setup
│   ├── test_car.py            Car model unit tests
│   ├── test_field.py          Field unit tests
│   ├── test_validators.py     Validator unit tests
│   ├── test_simulation.py     Simulation engine tests (scenarios 1 & 2)
│   └── test_integration.py    End-to-end CLI flow tests
├── docs/
│   └── assumptions_and_gaps.md
├── pyproject.toml
└── README.md
```

---

## Design Overview

### Architecture

| Module | Responsibility |
|---|---|
| `car.py` | Pure data model; no I/O or field awareness |
| `field.py` | Bounds checking; no car awareness |
| `simulation.py` | Orchestrates step execution and collision detection |
| `validators.py` | Parses and sanitises all user inputs |
| `main.py` | CLI loop; all `input()`/`print()` calls isolated here for testability |

### Collision Detection

At the end of each step, a position → car mapping is built. Any position occupied by 2+ active cars triggers a collision. All cars at that position are flagged with `collided = True` and cease processing.

### Boundary Handling

When a car's `next_position()` falls outside the field, the `F` command is silently ignored and the car retains its current position and direction.

---

## Assumptions

| ID | Assumption |
|---|---|
| A1 | `STEP_DEP_ID = 0` → The field origin is `(0,0)` (bottom-left); `(width-1, height-1)` is the top-right. A 10×10 field has valid coordinates 0–9 on each axis. |
| A2 | Commands are processed left-to-right within each step. Cars are processed in the order they were added. |
| A3 | If two cars start at the same initial position, a collision is detected at step 0 (before any commands run). This is treated as valid input — no upfront validation prevents it. |
| A4 | Car names are case-sensitive (`A` ≠ `a`). |
| A5 | Commands strings may be of different lengths. A car that exhausts its commands stays in its final position for the remaining steps. |
| A6 | If more than two cars collide at the same cell at the same step, each car's collision message lists all other cars at that cell. |
| A7 | Python 3.10+ is required (uses built-in `tuple[int, int]` generic type hints). |

---

## Gaps & Areas for Improvement

| ID | Gap | Recommendation |
|---|---|---|
| G1 | No duplicate initial-position validation | Warn (or error) if two cars are placed on the same cell before simulation starts |
| G2 | No maximum command length limit | Add a configurable cap to prevent extremely long command strings |
| G3 | CLI only — no file/batch input | Support `--input file.txt` flag to drive the simulation non-interactively for CI pipelines |
| G4 | No simulation replay / step-by-step mode | Add a `--step` flag to pause after each step and print intermediate state |
| G5 | Single unit number per session | Extend to support multiple named batch jobs / scenarios loaded from config |
| G6 | No logging | Integrate Python `logging` with configurable verbosity for production observability |
| G7 | `main.py` mixes I/O and control flow | Introduce a `Controller` class to fully decouple the CLI from the simulation engine, enabling a future GUI or API layer |
| G8 | Coverage of `main.py` via integration tests is limited | Refactor I/O into injectable `IOAdapter` for deterministic unit testing without `mock.patch` |
