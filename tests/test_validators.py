"""Tests for input validation helpers."""

import pytest
from auto_driving.validators import (
    parse_car_name,
    parse_commands,
    parse_field_dimensions,
    parse_initial_position,
)


class TestParseFieldDimensions:
    def test_valid(self):
        assert parse_field_dimensions("10 10") == (10, 10)

    def test_extra_spaces(self):
        assert parse_field_dimensions("  5  8  ") == (5, 8)

    def test_too_few_parts(self):
        with pytest.raises(ValueError):
            parse_field_dimensions("10")

    def test_too_many_parts(self):
        with pytest.raises(ValueError):
            parse_field_dimensions("10 10 10")

    def test_non_integer(self):
        with pytest.raises(ValueError):
            parse_field_dimensions("10 abc")

    def test_zero_dimension(self):
        with pytest.raises(ValueError):
            parse_field_dimensions("0 10")

    def test_negative_dimension(self):
        with pytest.raises(ValueError):
            parse_field_dimensions("-1 10")


class TestParseInitialPosition:
    def test_valid_north(self):
        assert parse_initial_position("1 2 N") == (1, 2, "N")

    def test_valid_south(self):
        assert parse_initial_position("0 0 S") == (0, 0, "S")

    def test_lowercase_direction(self):
        assert parse_initial_position("3 4 e") == (3, 4, "E")

    def test_invalid_direction(self):
        with pytest.raises(ValueError):
            parse_initial_position("1 2 X")

    def test_too_few_parts(self):
        with pytest.raises(ValueError):
            parse_initial_position("1 2")

    def test_non_integer_coords(self):
        with pytest.raises(ValueError):
            parse_initial_position("a b N")


class TestParseCommands:
    def test_valid_commands(self):
        assert parse_commands("FFRFFFFRRL") == "FFRFFFFRRL"

    def test_lowercase_normalised(self):
        assert parse_commands("fflr") == "FFLR"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            parse_commands("")

    def test_invalid_command_char(self):
        with pytest.raises(ValueError):
            parse_commands("FXL")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            parse_commands("   ")


class TestParseCarName:
    def test_valid_name(self):
        assert parse_car_name("A") == "A"

    def test_valid_with_underscore(self):
        assert parse_car_name("Car_1") == "Car_1"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            parse_car_name("")

    def test_space_in_name_raises(self):
        with pytest.raises(ValueError):
            parse_car_name("Car A")

    def test_special_chars_raise(self):
        with pytest.raises(ValueError):
            parse_car_name("Car-1")
