import re
from datetime import datetime, timedelta

from ...group import Group
from ...time import Time


class Valid(Group):
    """Basic structure for valid time groups in change periods and forecasts."""

    def __init__(self, match: re.Match, time: datetime) -> None:
        time = time.replace(minute=0)

        if match is None:
            super().__init__(None)

            time = time + timedelta(hours=1)

            self._from = Time(time=time)
            self._until = Time(time=time + timedelta(hours=24))
        else:
            super().__init__(match.string)

            _fmday: int = int(match.group("fmday"))
            _fmhour: int = int(match.group("fmhour"))
            _tlday: int = int(match.group("tlday"))
            _tlhour: int = int(match.group("tlhour"))

            _from: datetime
            _until: datetime
            if _fmday == time.day:
                _from = time
            else:
                _from = time + timedelta(days=1)

            if _tlday == time.day:
                _until = time
            else:
                _until = time + timedelta(days=1)

            if _tlhour == 24:
                _until = _until + timedelta(days=1)
                _tlhour = 0

            self._from = _from.replace(hour=_fmhour)
            self._until = _until.replace(hour=_tlhour)

    def __str__(self) -> str:
        return f"from {self._from} until {self._until}"

    @property
    def period_from(self) -> Time:
        """Get the time period `from` of the forecast."""
        return self._from

    @property
    def period_until(self) -> Time:
        """Get the time period `until` of the forecast."""
        return self._until


class TafValidMixin:
    """Mixin to add the valid period of forecast attribute and handler."""

    def __init__(self, time: datetime) -> None:
        self._valid = Valid(None, self._time.time)

    def _handle_valid_period(self, match: re.Match) -> None:
        self._valid = Valid(match, self._time.time)

        self._concatenate_string(self._valid)

    @property
    def valid(self) -> Valid:
        """Get the dates of valid period of the forecast."""
        return self._valid
