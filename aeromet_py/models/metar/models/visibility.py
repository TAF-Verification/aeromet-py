import re
from typing import Any, Dict, Optional

from ....utils import Conversions
from ...distance import Distance
from ...group import Group
from ...string_attribute import HasConcatenateStringProntocol
from ...wind import Direction


class MetarMinimumVisibility(Group):
    """Basic structure for minimum visibility groups in reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
        self._direction = Direction(None)

        if match is None:
            super().__init__(None)

            self._visibility = Distance(None)
        else:
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

    def _from_sea_miles(
        self, integer: Optional[str], fraction: Optional[str]
    ) -> Distance:
        """Helper to handle the visibility from sea miles.
        Args:
            integer (str | None): the integer value of visibility in METAR if provided.
            fraction (str | None): the fraction value of the visibility in METAR if provided.
        """
        _fraction: float
        if fraction:
            _items = fraction.split("/")
            _fraction = int(_items[0]) / int(_items[1])
        else:
            _fraction = 0.0

        _vis: float = _fraction

        if integer:
            _integer: float = float(integer)
            _vis += _integer

        return Distance("{}".format(_vis * Conversions.SMI_TO_KM * Conversions.KM_TO_M))

    def __str__(self) -> str:
        if self._visibility.value is None:
            return ""

        return "{:.1f} km{}".format(
            self.in_kilometers,
            f" to {self._direction.cardinal} ({self._direction})"
            if self._direction.value
            else "",
        )

    @property
    def in_meters(self) -> Optional[float]:
        """Get the visibility in meters."""
        return self._visibility.in_meters

    @property
    def in_kilometers(self) -> Optional[float]:
        """Get the visibility in kilometers."""
        return self._visibility.in_kilometers

    @property
    def in_sea_miles(self) -> Optional[float]:
        """Get the visibility in sea miles."""
        return self._visibility.in_sea_miles

    @property
    def in_feet(self) -> Optional[float]:
        """Get the visibility in feet."""
        return self._visibility.in_feet

    @property
    def cardinal_direction(self) -> Optional[str]:
        """Get the cardinal direction associated to the visibility, e.g. "NW" (north west)."""
        return self._direction.cardinal

    @property
    def direction_in_degrees(self) -> Optional[float]:
        """Get the visibility direction in degrees."""
        return self._direction.in_degrees

    @property
    def direction_in_radians(self) -> Optional[float]:
        """Get the visibility direction in radians."""
        return self._direction.in_radians

    @property
    def direction_in_gradians(self) -> Optional[float]:
        """Get the visibility direction in gradians."""
        return self._direction.in_gradians

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "visibility": self._visibility.to_dict(),
            "direction": self._direction.to_dict(),
        }
        d.update(super().to_dict())


class MetarPrevailingVisibility(MetarMinimumVisibility):
    """Basic structure for prevailing visibility in reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
        super().__init__(match)
        self._cavok = False

        if match:
            _cavok = match.group("cavok")
            if _cavok:
                self._cavok = True
                self._visibility = Distance("9999")

    def __str__(self) -> str:
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


class MetarPrevailingMixin(HasConcatenateStringProntocol):
    """Mixin to add prevailing visibility attribute to the report."""

    def __init__(self) -> None:
        self._prevailing = MetarPrevailingVisibility(None)

    def _handle_prevailing(self, match: re.Match) -> None:
        self._prevailing = MetarPrevailingVisibility(match)

        self._concatenate_string(self._prevailing)

    @property
    def prevailing_visibility(self) -> MetarPrevailingVisibility:
        """Get the prevailing visibility data of the report."""
        return self._prevailing
