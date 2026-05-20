"""Integration tests: simulate full CLI sessions via mocked I/O."""

import pytest
from unittest.mock import patch
from io import StringIO

from auto_driving.main import run_simulation_session


def run_with_inputs(*inputs: str) -> str:
    """Run one simulation session with the given input lines; return stdout."""
    input_stream = "\n".join(inputs) + "\n"
    with patch("builtins.input", side_effect=inputs):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            try:
                run_simulation_session()
            except (StopIteration, EOFError):
                pass
            return mock_out.getvalue()


class TestScenario1CLI:
    def test_single_car_final_position(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "1 2 N", "FFRFFFFRRL",
            "2",
            "2",
        )
        assert "A, (5,4) S" in output

    def test_field_confirmation_message(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "1 2 N", "F",
            "2", "2",
        )
        assert "You have created a field of 10 x 10." in output

    def test_car_list_shown_before_run(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "1 2 N", "F",
            "2", "2",
        )
        assert "A, (1,2) N, F" in output

    def test_after_simulation_shows_result_header(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "0 0 E", "F",
            "2", "2",
        )
        assert "After simulation, the result is:" in output


class TestScenario2CLI:
    def test_two_cars_collision(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "1 2 N", "FFRFFFFRRL",
            "1", "B", "7 8 W", "FFLFFFFFFF",
            "2",
            "2",
        )
        assert "collides with B at (5,4) at step 7" in output
        assert "collides with A at (5,4) at step 7" in output


class TestMenuNavigation:
    def test_invalid_menu_choice_reprompts(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "1 2 N", "F",
            "9",   # invalid
            "2",   # valid: run
            "2",
        )
        assert "Invalid option" in output

    def test_start_over_returns_true(self):
        with patch("builtins.input", side_effect=[
            "10 10", "1", "A", "0 0 N", "F", "2", "1"
        ]):
            result = run_simulation_session()
        assert result is True

    def test_exit_returns_false(self):
        with patch("builtins.input", side_effect=[
            "10 10", "1", "A", "0 0 N", "F", "2", "2"
        ]):
            result = run_simulation_session()
        assert result is False


class TestInputValidationCLI:
    def test_invalid_field_retries(self):
        output = run_with_inputs(
            "abc",       # bad
            "0 0",       # bad
            "10 10",     # good
            "1", "A", "1 1 N", "F",
            "2", "2",
        )
        assert "You have created a field of 10 x 10." in output

    def test_duplicate_car_name_rejected(self):
        output = run_with_inputs(
            "10 10",
            "1", "A", "0 0 N", "F",
            "1", "A",       # duplicate
            "B",            # new valid name
            "1 1 N", "F",
            "2", "2",
        )
        assert "already exists" in output

    def test_out_of_bounds_initial_position_rejected(self):
        output = run_with_inputs(
            "10 10",
            "1", "A",
            "15 15 N",   # out of bounds
            "1 1 N",     # valid
            "F",
            "2", "2",
        )
        assert "outside the field" in output
