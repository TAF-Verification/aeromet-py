import re

from datetime import datetime, timedelta
from typing import Any, Dict

from ..base import ChangeIndicator, Time
from .valid import Valid


class TafChangeIndicator(ChangeIndicator):
    """Basic structure for change indicators in TAF."""

    def __init__(self, match: re.Match, taf_valid: Valid) -> None:
        self._valid: Valid = taf_valid

        if match is None:
            super().__init__(None)
        else:
            if match.string.startswith("FM"):
                super().__init__(None)
                self._code = match.string

                day: int = int(match.group("day"))
                hour: int = int(match.group("hour"))
                minute: int = int(match.group("minute"))

                time: datetime = taf_valid.period_from.time
                while day != time.day:
                    time = time + timedelta(days=1)
                time = time.replace(hour=hour).replace(minute=minute)

                self._valid = Valid(None, Time(time=time), taf_valid.period_until)

                self._translation = f"{self._valid}"
            else:
                super().__init__(match)

    def set_valid_period(self, match: re.Match, init_time: Time) -> None:
        """Set the valid time period group of the change indicator.

        Args:
            match (re.Match): the match of the regular expression of valid time period.
            init_time (Time): the initial datetime of valid time of the forecast.
        """
        self._valid = Valid.from_taf(match, init_time.time)

        if self._code.startswith("FM"):
            self._translation = f"{self._valid}"
        else:
            self._translation = f"{self._translation} {self._valid}"
            self._code += f" {self._valid.code}"

    def reset_until_period(self, until: Time) -> None:
        """Reset the until time period of change indicators in the
        form `FMYYGGgg` only, because these haven't a group of valid
        time period.

        Args:
            until (Time): the until time period that this change indicator
            applies to.
        """
        until = Time(time=until.time - timedelta(hours=1))
        if self._code.startswith("FM"):
            self._valid = Valid(None, self._valid.period_from, until)
            self._translation = f"{self._valid}"

    @property
    def valid(self) -> Valid:
        """Get the valid period of the change indicator."""
        return self._valid

    def as_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "valid": self.valid.as_dict(),
        }
        d.update(super().as_dict())
        return d
