import re

from aeromet_py.utils import Conversions

from .descriptor import DataDescriptor
from .group import Group
from .numeric import Numeric


class Temperatures(Group):
    """Basic structure for temperatures in reports from land stations."""

    _temperature = DataDescriptor()
    _dewpoint = DataDescriptor()

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._temperature = Temperature(None)
            self._dewpoint = Temperature(None)
        else:
            super().__init__(match.string)

            _tsign: str = match.group("tsign")
            _temp: str = match.group("temp")
            _dsign: str = match.group("dsign")
            _dewpt: str = match.group("dewpt")

            self._temperature = self._set_temperature(_temp, _tsign)
            self._dewpoint = self._set_temperature(_dewpt, _dsign)

    def __str__(self) -> str:
        if self._temperature.value is None and self._dewpoint.value is None:
            return ""
        elif self._temperature.value is None and self._dewpoint.value:
            return f"no temperature | dewpoint: {self._dewpoint}"
        elif self._temperature.value is not None and self._dewpoint.value is None:
            return f"temperature: {self._temperature} | no dewpoint"
        else:
            return f"temperature: {self._temperature} | dewpoint: {self._dewpoint}"

    def _set_temperature(self, code: str, sign: str) -> "Temperature":
        """Hanlder to set the temperature value."""
        if sign in ["M", "-"]:
            return Temperature(f"-{code}")

        return Temperature(code)

    @property
    def temperature_in_celsius(self) -> float:
        """Returns the temperature in °Celsius."""
        return self._temperature.value

    @property
    def temperature_in_kelvin(self) -> float:
        """Returns the temperature in °Kelvin."""
        return self._temperature.converted(Conversions.celsius_to_kelvin)

    @property
    def temperature_in_fahrenheit(self) -> float:
        """Returns the temperature in °Fahrenheit."""
        return self._temperature.converted(Conversions.celsius_to_fahrenheit)

    @property
    def temperature_in_rankine(self) -> float:
        """Returns the temperature in Rankine."""
        return self._temperature.converted(Conversions.celsius_to_rankine)

    @property
    def dewpoint_in_celsius(self) -> float:
        """Returns the dewpoint in °Celsius."""
        return self._dewpoint.value

    @property
    def dewpoint_in_kelvin(self) -> float:
        """Returns the dewpoint in °Kelvin."""
        return self._dewpoint.converted(Conversions.celsius_to_kelvin)

    @property
    def dewpoint_in_fahrenheit(self) -> float:
        """Returns the dewpoint in °Fahrenheit."""
        return self._dewpoint.converted(Conversions.celsius_to_fahrenheit)

    @property
    def dewpoint_in_rankine(self) -> float:
        """Returns the dewpoint in Rankine."""
        return self._dewpoint.converted(Conversions.celsius_to_rankine)


class Temperature(Numeric):
    """Basic structure for temperature attributes."""

    def __init__(self, code: str) -> None:
        if code is None:
            code = "//"

        try:
            _temperature = float(code)
        except ValueError:
            _temperature = None
        finally:
            super().__init__(_temperature)

    def __str__(self) -> str:
        if self._value:
            return super().__str__() + "°C"

        return super().__str__()
