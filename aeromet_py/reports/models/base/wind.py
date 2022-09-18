import json
import re

from typing import Any, Dict, List, Optional

from aeromet_py.utils import Conversions

from .group import Group
from .numeric import Numeric


COMPASS_DIRS: Dict[str, List[float]] = {
    "NNE": [11.25, 33.75],
    "NE": [33.75, 56.25],
    "ENE": [56.25, 78.75],
    "E": [78.75, 101.25],
    "ESE": [101.25, 123.75],
    "SE": [123.75, 146.25],
    "SSE": [146.25, 168.75],
    "S": [168.75, 191.25],
    "SSW": [191.25, 213.75],
    "SW": [213.75, 236.25],
    "WSW": [236.25, 258.75],
    "W": [258.75, 281.25],
    "WNW": [281.25, 303.75],
    "NW": [303.75, 326.25],
    "NNW": [326.25, 348.75],
    "N": [348.75, 11.25],
}


class Direction(Numeric):
    """Basic structure for directions attributes."""

    def __init__(self, code: Optional[str]) -> None:
        if code is None or code == "//":
            code = "///"

        if len(code) == 2:
            code += "0"

        assert len(code) == 3, "wind direction code must have 3 or 2 digits length"

        self._variable = False

        try:
            _direction = float(code)
        except ValueError:
            if code == "VRB":
                self._variable = True
            _direction = None
        finally:
            super().__init__(_direction)

    def __str__(self) -> str:
        if self._variable:
            return "variable wind"

        if self._value:
            return super().__str__() + "°"

        return super().__str__()

    @classmethod
    def from_cardinal(cls, code: str) -> "Direction":
        """Classmethod to create a Direction object from a cardinal
        direction code.
        Raises:
            ValueError: Raised if code is not in COMPASS_DIRS keys.
        Returns:
            Direction: the Direction instance.
        """
        assert code != None, "code must be not None"

        if code == "N":
            return cls("360")

        for key in COMPASS_DIRS.keys():
            if key == code:
                mean_dir = round(sum(COMPASS_DIRS[key]) / 2)
                str_dir = "{:03d}".format(mean_dir)
                return cls(str_dir)

        raise ValueError(
            "invalid cardinal direction code, use one of the following: {}".format(
                COMPASS_DIRS.keys()
            )
        )

    @property
    def cardinal(self) -> Optional[str]:
        """Get the cardinal direction associated with the wind direction, e.g. "NW" (north west)"""
        value = self.converted(1)

        if value is None:
            return None

        north_dirs = COMPASS_DIRS["N"]
        if value >= north_dirs[0] or value < north_dirs[1]:
            return "N"

        for k, v in COMPASS_DIRS.items():
            if value >= v[0] and value < v[1]:
                return k

    @property
    def variable(self) -> bool:
        """Get if direction is `VRB` (variable) in the report."""
        return self._variable

    @property
    def in_degrees(self) -> Optional[float]:
        """Get the direction in degrees."""
        return self._value

    @property
    def in_radians(self) -> Optional[float]:
        """Get the direction in radians."""
        return self.converted(factor=Conversions.DEGREES_TO_RADIANS)

    @property
    def in_gradians(self) -> Optional[float]:
        """Get the direction in gradians."""
        return self.converted(factor=Conversions.DEGREES_TO_GRADIANS)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "cardinal": self.cardinal,
            "variable": self.variable,
            "units": "degrees",
            "direction": self.in_degrees,
        }


class Speed(Numeric):
    """Basic structure for speed attributes."""

    def __init__(self, code: Optional[str]) -> None:
        if code is None or code == "//":
            code = "///"

        if len(code) == 2:
            code = "0" + code

        assert len(code) >= 3, "wind speed code must have 2 or 3 digits length"

        try:
            _speed = float(code)
        except ValueError:
            _speed = None
        finally:
            super().__init__(_speed)

    def __str__(self) -> str:
        if self._value:
            return super().__str__() + " kt"

        return super().__str__()

    @property
    def in_knot(self) -> Optional[float]:
        """Get the speed in knot."""
        return self._value

    @property
    def in_mps(self) -> Optional[float]:
        """Get the speed in meters per second."""
        return self.converted(factor=Conversions.KNOT_TO_MPS)

    @property
    def in_kph(self) -> Optional[float]:
        """Get the speed in kilometers per hour."""
        return self.converted(factor=Conversions.KNOT_TO_KPH)

    @property
    def in_miph(self) -> Optional[float]:
        """Get the speed in miles per hour."""
        return self.converted(factor=Conversions.KNOT_TO_MIPH)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "units": "knot",
            "speed": self.in_knot,
        }


class Wind:
    """Basic structure for wind groups in report from land stations."""

    def __init__(
        self,
        direction: Optional[str] = None,
        speed: Optional[str] = None,
    ) -> None:
        self._direction = Direction(direction)
        self._speed = Speed(speed)

    def __str__(self) -> str:
        cardinal: str = self.cardinal_direction if self.cardinal_direction else ""

        direction: str = str(self._direction)
        direction = f"({self._direction})" if self._direction.value else direction

        s: str = "{} {} {}".format(
            cardinal,
            direction,
            self._speed,
        )
        s = re.sub(r"\s{2,}", " ", s)
        s = s.strip()

        return s

    def _mps2kt(self, value: str) -> str:
        """Helper to convert wind speed in meters per second to knots."""
        try:
            value_float = float(value)
        except (TypeError, ValueError):
            value = "///"
        else:
            value_int = value_float * Conversions.MPS_TO_KNOT
            value = "{}".format(value_int)

        return value

    @property
    def cardinal_direction(self) -> Optional[str]:
        """Returns the cardinal direction associated to the wind direction, e.g. "NW" (north west)."""
        return self._direction.cardinal

    @property
    def variable(self) -> bool:
        """Get if the wind direction is variable (VRB)."""
        return self._direction.variable

    @property
    def direction_in_degrees(self) -> Optional[float]:
        """Get the wind direction in degrees."""
        return self._direction.in_degrees

    @property
    def direction_in_radians(self) -> Optional[float]:
        """Get the wind direction in radians."""
        return self._direction.in_radians

    @property
    def direction_in_gradians(self) -> Optional[float]:
        """Get the wind direction in gradians."""
        return self._direction.in_gradians

    @property
    def speed_in_knot(self) -> Optional[float]:
        """Get the wind speed in knot."""
        return self._speed.in_knot

    @property
    def speed_in_mps(self) -> Optional[float]:
        """Get the wind speed in meters per second"""
        return self._speed.in_mps

    @property
    def speed_in_kph(self) -> Optional[float]:
        """Get the wind speed in kilometers per hour."""
        return self._speed.in_kph

    @property
    def speed_in_miph(self) -> Optional[float]:
        """Get the wind speed in miles per hour."""
        return self._speed.in_miph

    def as_dict(self) -> Dict[str, Dict[str, Any]]:
        return {
            "direction": self._direction.as_dict(),
            "speed": self._speed.as_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict())
