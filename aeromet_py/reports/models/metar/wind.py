import re

from typing import Any, Dict, Optional

from ..base import Group, HasConcatenateStringProntocol, Speed, Wind


class MetarWind(Wind, Group):
    """Basic structure for wind groups in METAR reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
        self._gust = Speed(None)

        if match is None:
            super().__init__()
            Group.__init__(self, None)
        else:
            _dir: str = match.group("dir")
            _spd: str = match.group("speed")
            _gst: str = match.group("gust")
            _unt: str = match.group("units")

            if _unt == "MPS":
                _spd = self._mps2kt(_spd)
                _gst = self._mps2kt(_gst)

            super().__init__(direction=_dir, speed=_spd)
            Group.__init__(self, match.string)
            self._gust = Speed(_gst)

    def __str__(self) -> str:
        gust: str = " gust of " + str(self._gust) if self._gust.value else ""

        return super().__str__() + gust

    @property
    def gust_in_knot(self) -> Optional[float]:
        """Get the wind gust in knot."""
        return self._gust.in_knot

    @property
    def gust_in_mps(self) -> Optional[float]:
        """Get the wind gust in meters per second"""
        return self._gust.in_mps

    @property
    def gust_in_kph(self) -> Optional[float]:
        """Get the wind gust in kilometers per hour."""
        return self._gust.in_kph

    @property
    def gust_in_miph(self) -> Optional[float]:
        """Get the wind gust in miles per hour."""
        return self._gust.in_miph

    def as_dict(self) -> Dict[str, Any]:
        d = super().as_dict()
        d.update({"gust": self._gust.as_dict()})
        d.update(Group.as_dict(self))
        return d


class MetarWindMixin(HasConcatenateStringProntocol):
    """Mixin to add a METAR wind group attribute to the report."""

    def __init__(self) -> None:
        self._wind = MetarWind(None)

    def _handle_wind(self, match: re.Match) -> None:
        self._wind = MetarWind(match)

        self._concatenate_string(self._wind)

    @property
    def wind(self) -> MetarWind:
        """Get the wind data of the report."""
        return self._wind
