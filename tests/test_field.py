"""Tests for the Field model."""

import pytest
from auto_driving.field import Field


class TestFieldCreation:
    def test_valid_field(self):
        f = Field(10, 10)
        assert f.width == 10
        assert f.height == 10

    def test_zero_width_raises(self):
        with pytest.raises(ValueError):
            Field(0, 10)

    def test_zero_height_raises(self):
        with pytest.raises(ValueError):
            Field(10, 0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            Field(-1, 5)

    def test_str(self):
        assert str(Field(10, 10)) == "10 x 10"


class TestBounds:
    @pytest.fixture
    def field(self):
        return Field(10, 10)

    def test_origin_in_bounds(self, field):
        assert field.is_within_bounds(0, 0)

    def test_top_right_in_bounds(self, field):
        assert field.is_within_bounds(9, 9)

    def test_x_equals_width_out_of_bounds(self, field):
        assert not field.is_within_bounds(10, 5)

    def test_y_equals_height_out_of_bounds(self, field):
        assert not field.is_within_bounds(5, 10)

    def test_negative_x_out_of_bounds(self, field):
        assert not field.is_within_bounds(-1, 5)

    def test_negative_y_out_of_bounds(self, field):
        assert not field.is_within_bounds(5, -1)
