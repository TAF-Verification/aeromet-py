import re
from typing import Any, Dict, Optional

from ...group import Group
from ...time import Time


class MetarTime(Time, Group):
    """Basic structure for time groups in METAR reports from land stations."""

    def __init__(
        self,
        match: Optional[re.Match] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
    ) -> None:

        if match is None:
            Group.__init__(self, None)
            super().__init__()
        else:
            day: str = match.group("day")
            hour: str = match.group("hour")
            minute: str = match.group("min")

            Group.__init__(self, match.string)
            super().__init__(day, hour, year=year, month=month, minute=minute)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update(Group.to_dict(self))
        return d


class MetarTimeMixin:
    """Basic structure to add `MetarTime` attribute to the report or section."""

    def __init__(self) -> None:
        self._time: MetarTime = MetarTime()  # type: ignore[override]
