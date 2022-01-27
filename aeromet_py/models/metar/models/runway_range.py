import re
from typing import Dict

from aeromet_py.utils.conversions import Conversions

from ...group import Group
from ...distance import Distance

NAMES: Dict[str, str] = {
    "R": "right",
    "L": "left",
    "C": "center",
}

RVR_LIMITS: Dict[str, str] = {
    "M": "below of",
    "P": "above of",
}

TRENDS: Dict[str, str] = {
    "N": "no change",
    "U": "increasing",
    "D": "decreasing",
}


class MetarRunwayRange(Group):
    """Basic structure to for runway range groups in reports from land stations."""

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._name = None
            self._rvr_low = None
            self._rvr_high = None
            self._trend = None
            self._low_range = Distance(None)
            self._high_range = Distance(None)
        else:
            super().__init__(match.string)

            self._rvr_low = RVR_LIMITS.get(match.group("rvrlow"), None)
            self._rvr_high = RVR_LIMITS.get(match.group("rvrhigh"), None)
            self._trend = TRENDS.get(match.group("trend"), None)

            _units: str = match.group("units")
            _low_range: str = match.group("low")
            _high_range: str = match.group("high")

            self._name = self._set_name(match.group("name"))
            self._low_range = self._set_range(_low_range, _units)
            self._high_range = self._set_range(_high_range, _units)

    def _set_name(self, code: str) -> str:
        """Helper to set the name of the runway."""
        if len(code) == 3:
            name_char = code[-1]
            name_str = NAMES.get(name_char, None)
            return code.replace(name_char, f" {name_str}")

        if code == "88":
            return "all runways"

        if code == "99":
            return "repeated"

        return code

    def _set_range(self, code: str, units: str) -> Distance:
        """Helper to set the visual range of the runway."""
        if code is None:
            return Distance(None)

        if units == "FT":
            _range: float = float(code)
            _range = _range * Conversions.FT_TO_M
            return Distance(f"{_range}")

        return Distance(code)

    def _range2str(self, _range: Distance, rvr: str) -> str:
        """Helper to represent the visual range as a string."""
        if _range.value is None:
            return ""

        if rvr:
            return "{} {}".format(rvr, _range)

        return "{}".format(_range)

    def __str__(self) -> str:
        if self._low_range.value is None:
            return ""

        return "runway {} {}{}{}".format(
            self._name,
            self.low_range,
            f" varying to {self.high_range}" if self._high_range.value else "",
            ", " + self._trend if self._trend else "",
        )

    @property
    def name(self) -> str:
        """Get the runway name."""
        return self._name

    @property
    def low_range(self) -> str:
        """Get the runway low range as a string."""
        return self._range2str(self._low_range, self._rvr_low)

    @property
    def low_in_meters(self) -> float:
        """Get the runway low range in meters."""
        return self._low_range.value

    @property
    def low_in_kilometers(self) -> float:
        """Get the runway low range in kilometers."""
        return self._low_range.converted(Conversions.M_TO_KM)

    @property
    def low_in_sea_miles(self) -> float:
        """Get the runway low range in sea miles."""
        return self._low_range.converted(Conversions.M_TO_SMI)

    @property
    def low_in_feet(self) -> float:
        """Get the runway low range in feet."""
        return self._low_range.converted(Conversions.M_TO_FT)

    @property
    def high_range(self) -> str:
        """Get the runway high range as a string."""
        return self._range2str(self._high_range, self._rvr_high)

    @property
    def high_in_meters(self) -> float:
        """Get the runway high range in meters."""
        return self._high_range.value

    @property
    def high_in_kilometers(self) -> float:
        """Get the runway high range in kilometers."""
        return self._high_range.converted(Conversions.M_TO_KM)

    @property
    def high_in_sea_miles(self) -> float:
        """Get the runway high range in sea miles."""
        return self._high_range.converted(Conversions.M_TO_SMI)

    @property
    def high_in_feet(self) -> float:
        """Get the runway high range in feet."""
        return self._high_range.converted(Conversions.M_TO_FT)

    @property
    def trend(self) -> str:
        """Get the trend of the runway range."""
        return self._trend