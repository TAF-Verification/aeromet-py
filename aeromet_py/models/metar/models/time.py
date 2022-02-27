import re

from aeromet_py.models.group import Group
from aeromet_py.models.time import Time


class MetarTime(Time, Group):
    """Basic structure for time groups in METAR reports from land stations."""

    def __init__(self, match: re.Match, year: int, month: int) -> None:

        if match is None:
            Group.__init__(self, None)
            super().__init__()
        else:
            day: str = match.group("day")
            hour: str = match.group("hour")
            minute: str = match.group("min")

            Group.__init__(self, match.string)
            super().__init__(day, hour, year=year, month=month, minute=minute)


class MetarTimeMixin:
    """Basic structure to add `MetarTime` attribute to the report or section."""

    def __init__(self) -> None:
        self._time: MetarTime = MetarTime(None, None, None)
