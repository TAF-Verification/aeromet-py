import re

from aeromet_py.utils import Conversions

from ...distance import Distance
from ...group import Group
from ...wind import Direction


class MetarMinimumVisibility(Group):
    """Basic structure for minimum visibility groups in reports from land stations."""

    def __init__(self, match: re.Match) -> None:
        self._direction = Direction(None)

        if match is None:
            super().__init__(None)

            self._visibility = Distance(None)
        else:
            print(match.string.replace("_", " "))
            super().__init__(match.string.replace("_", " "))

            _vis = match.group("vis")
            _dir = match.group("dir")
            _integer = match.group("integer")
            _fraction = match.group("fraction")
            _units = match.group("units")

            if _vis or _units == "M":
                self._visibility = Distance(_vis)

            if _integer or _fraction:
                if _units == "SM":
                    self._visibility = self._from_sea_miles(_integer, _fraction)

                if _units == "KM":
                    _in_meters = int(_integer) * 1000
                    self._visibility = Distance("{:04d}".format(_in_meters))

            if _dir:
                self._direction = Direction.from_cardinal(_dir)

    def _from_sea_miles(self, integer: str, fraction: str) -> Distance:
        """Helper to handle the visibility from sea miles.
        Args:
            integer (str): the integer value of visibility in METAR if provided.
            fraction (str): the fraction value of the visibility in METAR if provided.
        """
        if fraction:
            _items = fraction.split("/")
            _fraction: float = int(_items[0]) / int(_items[1])
        else:
            _fraction: float = 0.0

        _vis: float = _fraction

        if integer:
            _integer: float = float(integer)
            _vis += _integer

        return Distance("{}".format(_vis * Conversions.SMI_TO_KM * Conversions.KM_TO_M))

    def __str__(self):
        if self._visibility.value is None:
            return ""

        return "{:.1f} km{}".format(
            self.in_kilometers,
            f" to {self._direction.cardinal} ({self._direction})"
            if self._direction.value
            else "",
        )

    @property
    def in_meters(self) -> float:
        """Get the visibility in meters."""
        return self._visibility.value

    @property
    def in_kilometers(self) -> float:
        """Get the visibility in kilometers."""
        return self._visibility.converted(Conversions.M_TO_KM)

    @property
    def in_sea_miles(self) -> float:
        """Get the visibility in sea miles."""
        return self._visibility.converted(Conversions.M_TO_SMI)

    @property
    def in_feet(self) -> float:
        """Get the visibility in feet."""
        return self._visibility.converted(Conversions.M_TO_FT)

    @property
    def cardinal_direction(self) -> str:
        """Get the cardinal direction associated to the visibility, e.g. "NW" (north west)."""
        return self._direction.cardinal

    @property
    def direction_in_degrees(self) -> float:
        """Get the visibility direction in degrees."""
        return self._direction.value

    @property
    def direction_in_radians(self) -> float:
        """Get the visibility direction in radians."""
        return self._direction.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def direction_in_gradians(self) -> float:
        """Get the visibility direction in gradians."""
        return self._direction.converted(Conversions.DEGREES_TO_GRADIANS)


class MetarPrevailingVisibility(MetarMinimumVisibility):
    """Basic structure for prevailing visibility in reports from land stations."""

    def __init__(self, match: re.Match) -> None:
        super().__init__(match)
        self._cavok = False

        if match:
            _cavok = match.group("cavok")
            if _cavok:
                self._cavok = True
                self._visibility = Distance("9999")

    def __str__(self):
        if self._cavok:
            return "Ceiling and Visibility OK"

        return super().__str__()

    @property
    def cavok(self) -> bool:
        """Get True if CAVOK, False if not."""
        return self._cavok

    @cavok.setter
    def cavok(self, value: bool) -> None:
        """Sets the CAVOK attribute to `value`.
        Args:
            value (bool): the boolean to set.
        Raises:
            TypeError: if value is not instance of `bool` type, TypeError is raised.
        """
        if isinstance(value, bool):
            self._cavok = value
        else:
            raise TypeError("can't set cavok to {} type".format(type(value)))
