import re

from typing import Any, Dict, Optional

from ....utils import Conversions
from ..base import Distance, Group, Temperature


# Table 3700
SEA_STATE: Dict[str, str] = {
    "0": "calm (glassy)",
    "1": "calm (rippled)",
    "2": "smooth (wavelets)",
    "3": "slight",
    "4": "moderate",
    "5": "rough",
    "6": "very rough",
    "7": "high",
    "8": "very high",
    "9": "phenomenal",
}


class MetarSeaState(Group):
    """Basic structure for sea state data in METAR."""

    def __init__(self, match: Optional[re.Match]) -> None:
        if match is None:
            super().__init__(None)

            self._temperature = Temperature(None)
            self._state = None
            self._height = Distance(None)
        else:
            super().__init__(match.string)

            _sign: str = match.group("sign")
            _temp: str = match.group("temp")
            _state: str = match.group("state")
            _height: str = match.group("height")

            if _sign in ["M", "-"]:
                self._temperature = Temperature(f"-{_temp}")
            else:
                self._temperature = Temperature(_temp)

            self._state = SEA_STATE.get(_state, None)

            _height_as_float: float
            try:
                _height_as_float = int(_height) / 10
            except (ValueError, TypeError):
                _height_as_float = None
            finally:
                self._height = Distance(f"{_height_as_float}")

    def __str__(self) -> str:
        if (
            self._temperature.value is None
            and self._height.value is None
            and self._state is None
        ):
            return ""

        s: str = ""

        if self._temperature.value:
            s += f"temperature {self._temperature}, "
        else:
            s += "no temperature, "

        if self._height.value:
            s += f"significant wave height {self._height}, "
        else:
            s += "no significant wave height, "

        if self._state:
            s += f"{self._state}"
        else:
            s += "no sea state"

        return s

    @property
    def state(self) -> Optional[str]:
        """Get the sea state if provided in METAR."""
        return self._state

    @property
    def temperature_in_celsius(self) -> Optional[float]:
        """Get the temperature of the sea in Celsius."""
        return self._temperature.in_celsius

    @property
    def temperature_in_kelvin(self) -> Optional[float]:
        """Get the temperature of the sea in Kelvin."""
        return self._temperature.in_kelvin

    @property
    def temperature_in_fahrenheit(self) -> Optional[float]:
        """Get the temperature of the sea in Fahrenheit."""
        return self._temperature.in_fahrenheit

    @property
    def temperature_in_rankine(self) -> Optional[float]:
        """Get the temperature of the sea in Rankine."""
        return self._temperature.in_rankine

    @property
    def height_in_meters(self) -> Optional[float]:
        """Get the height of the significant wave in meters."""
        return self._height.in_meters

    @property
    def height_in_centimeters(self) -> Optional[float]:
        """Get the height of the significant wave in centimeters."""
        return self._height.converted(Conversions.M_TO_CM)

    @property
    def height_in_decimeters(self) -> Optional[float]:
        """Get the height of the significant wave in decimeters."""
        return self._height.converted(Conversions.M_TO_DM)

    @property
    def height_in_feet(self) -> Optional[float]:
        """Get the height of the significant wave in feet."""
        return self._height.converted(Conversions.M_TO_FT)

    @property
    def height_in_inches(self) -> Optional[float]:
        """Get the height of the significant wave in inches."""
        return self._height.converted(Conversions.M_TO_IN)

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "state": self.state,
            "temperature": self._temperature.as_dict(),
            "height": self._height.as_dict(),
        }
        d.update(super().as_dict())
        return d
