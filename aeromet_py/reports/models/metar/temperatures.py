import re

from typing import Any, Dict, Optional

from ..base import Group, Temperature


class MetarTemperatures(Group):
    """Basic structure for temperatures in METAR from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
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
    def temperature_in_celsius(self) -> Optional[float]:
        """Get the temperature in °Celsius."""
        return self._temperature.in_celsius

    @property
    def temperature_in_kelvin(self) -> Optional[float]:
        """Get the temperature in °Kelvin."""
        return self._temperature.in_kelvin

    @property
    def temperature_in_fahrenheit(self) -> Optional[float]:
        """Get the temperature in °Fahrenheit."""
        return self._temperature.in_fahrenheit

    @property
    def temperature_in_rankine(self) -> Optional[float]:
        """Get the temperature in Rankine."""
        return self._temperature.in_rankine

    @property
    def dewpoint_in_celsius(self) -> Optional[float]:
        """Get the dewpoint in °Celsius."""
        return self._dewpoint.in_celsius

    @property
    def dewpoint_in_kelvin(self) -> Optional[float]:
        """Get the dewpoint in °Kelvin."""
        return self._dewpoint.in_kelvin

    @property
    def dewpoint_in_fahrenheit(self) -> Optional[float]:
        """Get the dewpoint in °Fahrenheit."""
        return self._dewpoint.in_fahrenheit

    @property
    def dewpoint_in_rankine(self) -> Optional[float]:
        """Get the dewpoint in Rankine."""
        return self._dewpoint.in_rankine

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "temperature": self._temperature.as_dict(),
            "dewpoint": self._dewpoint.as_dict(),
        }
        d.update(super().as_dict())
        return d
