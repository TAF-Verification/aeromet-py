import re

from typing import Any, Dict, Optional

from ....utils import Conversions
from ..base import Direction, Group


class MetarWindVariation(Group):
    """Basic structure for wind variation groups in reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
        if match is None:
            super().__init__(None)

            self._from = Direction("///")
            self._to = Direction("///")
        else:
            super().__init__(match.string)

            self._from = Direction(match.group("from"))
            self._to = Direction(match.group("to"))

    def __str__(self) -> str:
        if self._from.value is None:
            return ""

        return "from {} ({}) to {} ({})".format(
            self._from.cardinal,
            self._from,
            self._to.cardinal,
            self._to,
        )

    @property
    def from_cardinal_direction(self) -> Optional[str]:
        """Get the `from` cardinal direction, e.g. "NW" (north west)."""
        return self._from.cardinal

    @property
    def from_in_degrees(self) -> Optional[float]:
        """Get the `from` direction in degrees."""
        return self._from.value

    @property
    def from_in_radians(self) -> Optional[float]:
        """Get the `from` direction in radians."""
        return self._from.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def from_in_gradians(self) -> Optional[float]:
        """Get the `from` direction in gradians."""
        return self._from.converted(Conversions.DEGREES_TO_GRADIANS)

    @property
    def to_cardinal_direction(self) -> Optional[str]:
        """Get the `to` cardinal direction, e.g. "NW" (north west)."""
        return self._to.cardinal

    @property
    def to_in_degrees(self) -> Optional[float]:
        """Get the `to` direction in degrees."""
        return self._to.value

    @property
    def to_in_radians(self) -> Optional[float]:
        """Get the `to` direction in radians."""
        return self._to.converted(Conversions.DEGREES_TO_RADIANS)

    @property
    def to_in_gradians(self) -> Optional[float]:
        """Get the `to` direction in gradians."""
        return self._to.converted(Conversions.DEGREES_TO_GRADIANS)

    def as_dict(self) -> Dict[str, Dict[str, Any]]:
        d = {
            "from_": self._from.as_dict(),
            "to": self._to.as_dict(),
        }
        d.update(super().as_dict())
        return d
