"""Tests for the Simulator engine."""

import pytest
from auto_driving.car import Car
from auto_driving.field import Field
from auto_driving.simulation import Simulator


def make_field(w=10, h=10):
    return Field(w, h)


class TestScenario1SingleCar:
    """Spec scenario 1: single car, no collision."""

    def test_spec_example(self):
        """Car A at (1,2) N with FFRFFFFRRL → (5,4) S"""
        field = make_field()
        car = Car("A", 1, 2, "N", "FFRFFFFRRL")
        result = Simulator(field, [car]).run()
        assert result.get("A") == "- A, (5,4) S"

    def test_car_facing_preserved_correctly(self):
        field = make_field()
        car = Car("A", 0, 0, "E", "FFF")
        Simulator(field, [car]).run()
        assert car.x == 3
        assert car.y == 0
        assert car.direction == "E"

    def test_boundary_ignored_south_at_origin(self):
        """Car at (0,0) facing S: F command ignored, stays put."""
        field = make_field()
        car = Car("A", 0, 0, "S", "F")
        Simulator(field, [car]).run()
        assert car.x == 0
        assert car.y == 0

    def test_boundary_ignored_west_at_origin(self):
        field = make_field()
        car = Car("A", 0, 0, "W", "F")
        Simulator(field, [car]).run()
        assert car.x == 0
        assert car.y == 0

    def test_boundary_ignored_north_at_top(self):
        field = make_field(10, 10)
        car = Car("A", 0, 9, "N", "F")
        Simulator(field, [car]).run()
        assert car.y == 9  # stays

    def test_boundary_ignored_east_at_right(self):
        field = make_field(10, 10)
        car = Car("A", 9, 0, "E", "F")
        Simulator(field, [car]).run()
        assert car.x == 9  # stays

    def test_car_with_no_commands(self):
        """Edge case: car has no commands, stays at initial position."""
        field = make_field()
        car = Car("A", 3, 3, "N", "F")
        # Override to empty after construction (validators prevent empty)
        car.commands = ""
        Simulator(field, [car]).run()
        assert car.x == 3
        assert car.y == 3

    def test_only_turns(self):
        field = make_field()
        car = Car("A", 5, 5, "N", "LLLL")
        Simulator(field, [car]).run()
        assert car.x == 5
        assert car.y == 5
        assert car.direction == "N"


class TestScenario2MultipleCarCollision:
    """Spec scenario 2: two cars, detect collision."""

    def test_spec_example_collision(self):
        """
        A at (1,2) N with FFRFFFFRRL
        B at (7,8) W with FFLFFFFFFF
        → both collide at (5,4) at step 7
        """
        field = make_field()
        car_a = Car("A", 1, 2, "N", "FFRFFFFRRL")
        car_b = Car("B", 7, 8, "W", "FFLFFFFFFF")
        result = Simulator(field, [car_a, car_b]).run()
        assert result.get("A") == "- A, collides with B at (5,4) at step 7"
        assert result.get("B") == "- B, collides with A at (5,4) at step 7"

    def test_no_collision_when_paths_dont_cross(self):
        field = make_field()
        car_a = Car("A", 0, 0, "E", "FFF")
        car_b = Car("B", 9, 9, "W", "FFF")
        result = Simulator(field, [car_a, car_b]).run()
        assert "collides" not in result.get("A")
        assert "collides" not in result.get("B")

    def test_collided_cars_stop_moving(self):
        """After collision, cars must not continue moving."""
        field = make_field(10, 10)
        # Both start one step away from collision point
        car_a = Car("A", 4, 5, "E", "FFFFFF")
        car_b = Car("B", 6, 5, "W", "FFFFFF")
        Simulator(field, [car_a, car_b]).run()
        # They should meet at (5,5) at step 1 — both stop there
        assert car_a.x == 5 and car_a.y == 5
        assert car_b.x == 5 and car_b.y == 5
        assert car_a.collided
        assert car_b.collided

    def test_shorter_commands_car_stays_put(self):
        """Car with fewer commands stops after its last command."""
        field = make_field()
        car_a = Car("A", 0, 0, "E", "F")     # only 1 command
        car_b = Car("B", 9, 0, "W", "FFF")   # 3 commands
        result = Simulator(field, [car_a, car_b]).run()
        # A ends at (1,0), B ends at (6,0) — no collision
        assert "collides" not in result.get("A")
        assert "collides" not in result.get("B")
        assert car_a.x == 1
        assert car_b.x == 6

    def test_three_cars_all_collide_at_same_point(self):
        """Three cars converging on the same cell at the same step."""
        field = make_field(10, 10)
        car_a = Car("A", 4, 5, "E", "F")
        car_b = Car("B", 6, 5, "W", "F")
        car_c = Car("C", 5, 4, "N", "F")
        result = Simulator(field, [car_a, car_b, car_c]).run()
        for name in ("A", "B", "C"):
            assert "collides" in result.get(name)

    def test_result_all_results_order_preserved(self):
        """Results are returned in car-insertion order."""
        field = make_field()
        cars = [
            Car("A", 0, 0, "E", "F"),
            Car("B", 5, 0, "E", "F"),
            Car("C", 8, 0, "E", "F"),
        ]
        result = Simulator(field, cars).run()
        names = [r.split(",")[0].lstrip("- ") for r in result.all_results()]
        assert names == ["A", "B", "C"]


class TestCommandProcessingOrder:
    """Step-by-step interleaving per spec."""

    def test_commands_interleaved_per_step(self):
        """
        Verify step-by-step interleaving by checking intermediate positions
        conceptually via final outcome.
        A and B both move East; at step 1 A goes first, then B.
        Neither collides; final positions are independent.
        """
        field = make_field()
        car_a = Car("A", 0, 0, "E", "FF")
        car_b = Car("B", 3, 0, "E", "FF")
        Simulator(field, [car_a, car_b]).run()
        assert car_a.x == 2
        assert car_b.x == 5
