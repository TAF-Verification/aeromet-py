from ..utils import Conversions
from .numeric import Numeric


class Temperature(Numeric):
    """Basic structure for temperature attributes."""

    def __init__(self, code: str) -> None:
        if code is None or code in ["//", "///"]:
            code = "///"

        if len(code.replace("-", "")) == 2:
            code += "0"

        assert (
            len(code.replace("-", "")) == 3
        ), "temperature code must have 3 or 2 digits length"

        try:
            _temperature = float(code) / 10
        except ValueError:
            _temperature = None
        finally:
            super().__init__(_temperature)

    def __str__(self) -> str:
        if self._value:
            return super().__str__() + "°C"

        return super().__str__()

    @property
    def in_celsius(self) -> float:
        """Get the temperature in Celsius."""
        return self._value

    @property
    def in_kelvin(self) -> float:
        """Get the temperature in Kelvin"""
        return self.converted(Conversions.celsius_to_kelvin)

    @property
    def in_fahrenheit(self) -> float:
        """Get the temperature in Fahrenheit."""
        return self.converted(Conversions.celsius_to_fahrenheit)

    @property
    def in_rankine(self) -> float:
        """Get the temperature in Rankine."""
        return self.converted(Conversions.celsius_to_rankine)
