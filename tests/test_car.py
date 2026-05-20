"""Tests for the Car model."""

import pytest
from auto_driving.car import Car


@pytest.fixture
def car_north():
    return Car(name="A", x=1, y=2, direction="N", commands="FFRFFFFRRL")


class TestTurning:
    def test_turn_left_N_gives_W(self, car_north):
        car_north.turn_left()
        assert car_north.direction == "W"

    def test_turn_right_N_gives_E(self, car_north):
        car_north.turn_right()
        assert car_north.direction == "E"

    def test_full_left_rotation(self, car_north):
        for expected in ["W", "S", "E", "N"]:
            car_north.turn_left()
            assert car_north.direction == expected

    def test_full_right_rotation(self, car_north):
        for expected in ["E", "S", "W", "N"]:
            car_north.turn_right()
            assert car_north.direction == expected


class TestNextPosition:
    def test_north(self):
        car = Car("A", 3, 3, "N", "F")
        assert car.next_position() == (3, 4)

    def test_south(self):
        car = Car("A", 3, 3, "S", "F")
        assert car.next_position() == (3, 2)

    def test_east(self):
        car = Car("A", 3, 3, "E", "F")
        assert car.next_position() == (4, 3)

    def test_west(self):
        car = Car("A", 3, 3, "W", "F")
        assert car.next_position() == (2, 3)


class TestCarStr:
    def test_str_representation(self, car_north):
        assert str(car_north) == "- A, (1,2) N, FFRFFFFRRL"


class TestCollisionState:
    def test_initially_not_collided(self, car_north):
        assert car_north.collided is False
        assert car_north.collision_info is None
