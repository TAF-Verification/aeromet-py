import re

from typing import Any, Dict, Optional

from ...group import Group
from ...string_attribute import HasConcatenateStringProntocol
from ...wind import Wind


class MetarWind(Wind, Group):
    """Basic structure for wind groups in METAR reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
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

            super().__init__(direction=_dir, speed=_spd, gust=_gst)
            Group.__init__(self, match.string)

    def as_dict(self) -> Dict[str, Any]:
        d = super().as_dict()
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
