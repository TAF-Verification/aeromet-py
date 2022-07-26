import re

from typing import Optional

from ....utils import Conversions
from ..base import Group, Pressure


class MetarPressure(Pressure, Group):
    """Basic structure for pressure in METAR from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
        if match is None:
            super().__init__(None)
            Group.__init__(self, None)
        else:
            Group.__init__(self, match.string)

            _units: str = match.group("units")
            _press: str = match.group("press")
            _unit2: str = match.group("units2")

            if _press != "////":
                _pressure: float = float(_press)

                if _units == "A" or _unit2 == "INS":
                    _pressure = _pressure / 100.0 * Conversions.INHG_TO_HPA
                elif _units in ["Q", "QNH"]:
                    _pressure = _pressure * 1
                elif _pressure > 2500.0:
                    _pressure = _pressure * Conversions.INHG_TO_HPA
                else:
                    _pressure = _pressure * Conversions.MBAR_TO_HPA

                _press = f"{_pressure:.10f}"

            super().__init__(_press)
