import re
from typing import Dict

from ...temperature import Temperature
from ...group import Group

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

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._temperature = Temperature(None)
            self._state = None
        else:
            super().__init__(match.string)

            _sign: str = match.group("sign")
            _temp: str = match.group("temp")
            _state: str = match.group("state")

            if _sign in ["M", "-"]:
                self._temperature = Temperature(f"-{_temp}")
            else:
                self._temperature = Temperature(_temp)

            self._state = SEA_STATE.get(_state, None)

    def __str__(self) -> str:
        if self._temperature.value is None and self._state:
            return f"no temperature, {self.state}"
        elif self._temperature.value and self._state is None:
            return "temperature {}, no sea state".format(self._temperature)
        elif self._temperature.value is None and self._state is None:
            return ""
        else:
            return "temperature {}, {}".format(
                self._temperature,
                self._state,
            )

    @property
    def state(self) -> str:
        """Get the sea state if provided in METAR."""
        return self._state

    @property
    def temperature_in_celsius(self) -> float:
        """Get the temperature of the sea in Celsius."""
        return self._temperature.in_celsius

    @property
    def temperature_in_kelvin(self) -> float:
        """Get the temperature of the sea in Kelvin."""
        return self._temperature.in_kelvin

    @property
    def temperature_in_fahrenheit(self) -> float:
        """Get the temperature of the sea in Fahrenheit."""
        return self._temperature.in_fahrenheit

    @property
    def temperature_in_rankine(self) -> float:
        """Get the temperature of the sea in Rankine."""
        return self._temperature.in_rankine
