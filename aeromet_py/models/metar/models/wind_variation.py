import re

from aeromet_py.utils import Conversions

from ...group import Group
from ...wind import Direction


class WindVariation(Group):
    """Basic structure for wind variation groups in reports from land stations."""

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._from = Direction("///")
            self._to = Direction("///")
        else:
            super().__init__(match.string)

            self._from = Direction(match.group("from"))
            self._to = Direction(match.group("to"))

    def __str__(self):
        if self._from.value is None:
            return ""

        return "from {} ({}) to {} ({})".format(
            self._from.cardinal,
            self._from,
            self._to.cardinal,
            self._to,
        )

    @property
    def from_cardinal_direction(self) -> str:
        """Get the `from` cardinal direction, e.g. "NW" (north west)."""
        return self._from.cardinal

    @property
    def from_in_degrees(self) -> float:
        """Get the `from` direction in degrees."""
        return self._from.value

    @property
    def from_in_radians(self) -> float:
        """Get the `from` direction in radians."""
        return self._from.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def from_in_gradians(self) -> float:
        """Get the `from` direction in gradians."""
        return self._from.converted(Conversions.DEGREES_TO_GRADIANS)

    @property
    def to_cardinal_direction(self) -> str:
        """Get the `to` cardinal direction, e.g. "NW" (north west)."""
        return self._to.cardinal

    @property
    def to_in_degrees(self) -> float:
        """Get the `to` direction in degrees."""
        return self._to.value

    @property
    def to_in_radians(self) -> float:
        """Get the `to` direction in radians."""
        return self._to.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def to_in_gradians(self) -> float:
        """Get the `to` direction in gradians."""
        return self._to.converted(Conversions.DEGREES_TO_GRADIANS)