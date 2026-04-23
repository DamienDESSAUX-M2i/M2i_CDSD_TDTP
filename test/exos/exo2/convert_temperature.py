from typing import Callable, Dict, Literal

TemperatureUnit = Literal["C", "F", "K"]

Converter = Callable[[float], float]


def _c_to_f(value: float) -> float:
    return (value * 9 / 5) + 32


def _f_to_c(value: float) -> float:
    return (value - 32) * 5 / 9


def _c_to_k(value: float) -> float:
    return value + 273.15


def _k_to_c(value: float) -> float:
    return value - 273.15


TO_CELSIUS: Dict[TemperatureUnit, Converter] = {
    "C": lambda x: x,
    "F": _f_to_c,
    "K": _k_to_c,
}

FROM_CELSIUS: Dict[TemperatureUnit, Converter] = {
    "C": lambda x: x,
    "F": _c_to_f,
    "K": _c_to_k,
}


def convert_temperature(
    value: float,
    unit_source: TemperatureUnit,
    unit_target: TemperatureUnit,
) -> float:
    """Convert a temperature between Celsius, Fahrenheit, and Kelvin.

    Conversion is performed via Celsius as an intermediate unit using
    composable transformation functions.

    Args:
        value (float): The temperature value to convert.
        unit_source (TemperatureUnit): Source unit ("C", "F", or "K").
        unit_target (TemperatureUnit): Target unit ("C", "F", or "K").

    Returns:
        float: Converted temperature rounded to 2 decimal places.

    Raises:
        ValueError: If either unit is invalid.

    Examples:
        >>> convert_temperature(0, "C", "F")
        32.0
        >>> convert_temperature(32, "F", "C")
        0.0
    """
    if unit_source not in TO_CELSIUS or unit_target not in FROM_CELSIUS:
        raise ValueError("Invalid unit. Use 'C', 'F', or 'K'.")

    if unit_source == unit_target:
        return round(value, 2)

    celsius = TO_CELSIUS[unit_source](value)
    result = FROM_CELSIUS[unit_target](celsius)

    return round(result, 2)
