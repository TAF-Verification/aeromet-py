import re

from aeromet_py.models.group import Group
from aeromet_py.models.time import Time


class MetarTime(Time, Group):
    """Basic structure for time groups in METAR reports from land stations."""

    def __init__(self, match: re.Match, year: int, month: int) -> None:
        Group.__init__(self, match.string)

        if match is None:
            super().__init__()
        else:
            day: str = match.group("day")
            hour: str = match.group("hour")
            minute: str = match.group("min")

            super().__init__(day, hour, year=year, month=month, minute=minute)
