import pytest
from convert_temperature import convert_temperature


@pytest.mark.parametrize(
    "value, source, target, expected",
    [
        (0, "C", "F", 32.0),
        (100, "C", "F", 212.0),
        (0, "C", "K", 273.15),
        (32, "F", "C", 0.0),
        (212, "F", "C", 100.0),
        (32, "F", "K", 273.15),
        (273.15, "K", "C", 0.0),
        (273.15, "K", "F", 32.0),
        (-273.15, "C", "K", 0.0),
    ],
)
def test_convert_temperature_valid_inputs_returns_expected_value(
    value, source, target, expected
):
    assert convert_temperature(value, source, target) == expected


@pytest.mark.parametrize("unit", ["C", "F", "K"])
def test_convert_temperature_same_unit_returns_rounded_input(unit):
    value = 42.1234
    result = convert_temperature(value, unit, unit)
    assert result == round(value, 2)


@pytest.mark.parametrize(
    "value, source, target",
    [
        (42, "X", "C"),
        (42, "C", "X"),
        (42, "A", "B"),
    ],
)
def test_convert_temperature_invalid_units_raises_value_error(value, source, target):
    with pytest.raises(ValueError):
        convert_temperature(value, source, target)


@pytest.mark.parametrize(
    "value, unit_a, unit_b",
    [
        (0, "C", "F"),
        (100, "C", "K"),
        (32, "F", "K"),
        (273.15, "K", "F"),
        (-40, "C", "F"),
    ],
)
def test_convert_temperature_round_trip_conversion_returns_original_value(
    value, unit_a, unit_b
):
    forward = convert_temperature(value, unit_a, unit_b)
    backward = convert_temperature(forward, unit_b, unit_a)

    assert backward == pytest.approx(round(value, 2), abs=1e-2)


@pytest.mark.parametrize(
    "value",
    [-273.15, -100, 0, 37, 1000],
)
def test_convert_temperature_celsius_to_kelvin_to_celsius_returns_original_value(value):
    kelvin = convert_temperature(value, "C", "K")
    celsius = convert_temperature(kelvin, "K", "C")

    assert celsius == pytest.approx(round(value, 2), abs=1e-2)


def test_convert_temperature_valid_input_applies_rounding_to_two_decimals():
    result = convert_temperature(1, "C", "F")
    assert isinstance(result, float)
    assert round(result, 2) == result
