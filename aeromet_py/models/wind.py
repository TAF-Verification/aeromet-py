import re

from .descriptor import DataDescriptor
from .errors import ParserError
from .numeric import Numeric
from .group import Group
from aeromet_py.utils import Conversions

COMPASS_DIRS = {
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


class Wind(Group):

    _direction = DataDescriptor()
    _speed = DataDescriptor()
    _gust = DataDescriptor()

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._direction = Direction("///")
            self._speed = Speed("///")
            self._gust = Speed("///")
        else:
            super().__init__(match.string)

            self._direction = Direction(match.group("dir"))
            units: str = match.group("units")

            if units == "KT":
                self._speed = Speed(match.group("speed"))
                self._gust = Speed(match.group("gust"))

            if units == "MPS":
                speed = match.group("speed")
                gust = match.group("gust")

                speed = self._speed_in_mps_to_kt(speed)
                gust = self._speed_in_mps_to_kt(gust)

                self._speed = Speed(speed)
                self._gust = Speed(gust)

    def __str__(self):
        cardinal: str = self.cardinal_direction if self.cardinal_direction else ""

        direction: str = str(self._direction)
        direction = f"({self._direction})" if self._direction.value else direction

        gust: str = "gusts of " + str(self._gust) if self._gust.value else ""

        s: str = "{} {} {} {}".format(
            cardinal,
            direction,
            self._speed,
            gust,
        )
        s = re.sub(r"\s{2,}", " ", s)
        s = s.strip()

        return s

    def _speed_in_mps_to_kt(self, value: str) -> str:
        """Helper to convert wind speed in meters per second to knots."""
        try:
            value_float = float(value)
        except (TypeError, ValueError):
            value = "///"
        else:
            value_int = round(value_float * Conversions.MPS_TO_KNOT)
            value = "{:03d}".format(value_int)

        return value

    @property
    def cardinal_direction(self) -> str:
        """Returns the cardinal direction associated to the wind direction.

        Returns:
            str: the cardinal direction, e.g. "NW" (north west)
        """
        value = self._direction.converted(1)

        if value is not None:
            north_dirs = COMPASS_DIRS["N"]
            if value >= north_dirs[0] or value < north_dirs[1]:
                return "N"

            for k, v in COMPASS_DIRS.items():
                if value >= v[0] and value < v[1]:
                    return k

        return None

    @property
    def variable_wind(self) -> bool:
        """Returns if the wind direction is variable in report."""
        return self._direction.variable

    @property
    def direction_in_degrees(self) -> float:
        """Returns the wind direction in degrees."""
        return self._direction.value

    @property
    def direction_in_radians(self) -> float:
        """Returns the wind direction in radians."""
        return self._direction.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def direction_in_gradians(self) -> float:
        """Returns the wind direction in gradians."""
        return self._direction.converted(Conversions.DEGREES_TO_GRADIANS)

    @property
    def speed_in_mps(self) -> float:
        """Returns the wind speed in meters per second."""
        return self._speed.converted(Conversions.KNOT_TO_MPS)

    @property
    def speed_in_knot(self) -> float:
        """Returns the wind speed in knots."""
        return self._speed.value

    @property
    def speed_in_kph(self) -> float:
        """Returns the wind speed in kilometers per hour."""
        return self._speed.converted(Conversions.KNOT_TO_KPH)

    @property
    def speed_in_miph(self) -> float:
        """Returns the wind speed in miles per hour."""
        return self._speed.converted(Conversions.KNOT_TO_MIPH)

    @property
    def gust_in_mps(self) -> float:
        """Returns the wind gusts in meters per second."""
        return self._gust.converted(Conversions.KNOT_TO_MPS)

    @property
    def gust_in_knot(self) -> float:
        """Returns the wind gusts in knots."""
        return self._gust.value

    @property
    def gust_in_kph(self) -> float:
        """Returns the wind gusts in kilometers per hour."""
        return self._gust.converted(Conversions.KNOT_TO_KPH)

    @property
    def gust_in_miph(self) -> float:
        """Returns the wind gusts in miles per hour."""
        return self._gust.converted(Conversions.KNOT_TO_MIPH)


class Direction(Numeric):

    _variable = DataDescriptor()

    def __init__(self, code: str) -> None:
        if code is None:
            code = "///"

        if len(code) == 2:
            code = code + "0"

        assert len(code) == 3, "wind direction code must have 3 or 2 digits length"

        try:
            _direction = float(code)
            self._variable = False
        except ValueError:
            if code == "VRB":
                self._variable = True
            else:
                self._variable = False
            _direction = None
        finally:
            super().__init__(_direction)

    def __str__(self) -> str:
        if self._variable:
            return "variable wind"

        if self._value:
            return super().__str__() + "°"

        return super().__str__()

    @property
    def variable(self) -> bool:
        """Returns True if direction is `VRB` in the report.
        False otherwise."""
        return self._variable


class Speed(Numeric):
    def __init__(self, code: str) -> None:
        if code is None:
            code = "///"

        if len(code) == 2:
            code = "0" + code

        assert len(code) == 3, "wind speed code must have 2 or 3 digits length"

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
