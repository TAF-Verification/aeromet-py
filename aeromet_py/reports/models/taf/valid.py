import re

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from typing_extensions import Protocol

from ..base import Group, HasConcatenateStringProntocol, Time


class Valid(Group):
    """Basic structure for valid time groups in change periods and forecasts."""

    def __init__(self, code: str, from_: Time, until_: Time) -> None:
        super().__init__(code)
        self._from = from_
        self._until = until_

    @classmethod
    def from_taf(cls, match: Optional[re.Match], time: datetime) -> "Valid":
        """Returns an instance of the Valid class using a TAF like
        group of valid period of time.

        Args:
            match (re.Match): the match of the regular expression.
            time (datetime): the initial valid time of the forecast.

        Returns:
            Valid: the instance of the Valid class.
        """
        time = time.replace(minute=0)

        if match is None:
            time = time + timedelta(hours=1)

            return cls(
                None,
                Time(time=time),
                Time(time=time + timedelta(hours=24)),
            )
        else:
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

            return cls(
                match.string,
                Time(time=_from.replace(hour=_fmhour)),
                Time(time=_until.replace(hour=_tlhour)),
            )

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

    @property
    def duration(self) -> timedelta:
        """Get the validity of the forecast."""
        return self._until.time - self._from.time

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "from_": self.period_from.as_dict(),
            "until": self.period_until.as_dict(),
        }
        d.update(super().as_dict())
        return d


class HasTimeProtocol(Protocol):
    _time: Time


class TafValidMixin(HasConcatenateStringProntocol, HasTimeProtocol):
    """Mixin to add the valid period of forecast attribute and handler."""

    def __init__(self) -> None:
        self._valid = Valid.from_taf(None, self._time.time)

    def _handle_valid_period(self, match: re.Match) -> None:
        self._valid = Valid.from_taf(match, self._time.time)

        self._concatenate_string(self._valid)

    @property
    def valid(self) -> Valid:
        """Get the dates of valid period of the forecast."""
        return self._valid
