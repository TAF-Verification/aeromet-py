import re

from aeromet_py.models.group import Group
from aeromet_py.models.wind import Wind


class MetarWind(Wind, Group):
    """Basic structure for wind groups in METAR reports from land stations."""

    def __init__(self, match: re.Match) -> None:
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