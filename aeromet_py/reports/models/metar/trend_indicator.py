import re

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

from ..base import ChangeIndicator, Time


class MetarTrendIndicator(ChangeIndicator):
    """Basic structure for trend codes in METAR."""

    def __init__(self, match: Optional[re.Match], time: datetime) -> None:
        super().__init__(match)

        # Init period and end period of forecast
        self._init_period = Time(time=time)
        self._end_period = Time(time=self._init_period.time + timedelta(hours=2))

        self._from: Time = self._init_period
        self._until: Time = self._end_period
        self._at: Optional[Time] = None

    def __str__(self) -> str:
        if self._at:
            return super().__str__() + f" at {self._at}"

        if self._translation:
            return super().__str__() + f" from {self._from} until {self._until}"

        return super().__str__()

    def add_period(self, match: re.Match) -> None:
        """Helper to add periods of time to the change indicator."""
        self._code += f" {match.string}"

        # The middle time between self._init_period and self._end_period
        middle_time: datetime = self._init_period.time + timedelta(hours=1)

        prefix: str = match.group("prefix")
        hour: str = match.group("hour")
        minute: str = match.group("min")

        hour_as_int: int = int(hour)
        min_as_int: int = int(minute)

        _time: datetime
        minutes: int
        if hour_as_int == self._init_period.hour:
            minutes = min_as_int - self._init_period.minute
            _time = self._init_period.time + timedelta(minutes=minutes)
        elif hour_as_int == middle_time.hour:
            minutes = min_as_int - middle_time.minute
            _time = middle_time + timedelta(minutes=minutes)
        else:
            minutes = min_as_int - self._end_period.minute
            _time = self._end_period.time + timedelta(minutes=minutes)

        if prefix == "FM":
            self._from = Time(code=match.string, time=_time)
        elif prefix == "TL":
            self._until = Time(code=match.string, time=_time)
        else:
            self._at = Time(code=match.string, time=_time)

    @property
    def forecast_period(self) -> Tuple[Time, Time]:
        """Get the forcast period, i.e. the initial forecast time and the end forecast time."""
        return self._init_period, self._end_period

    @property
    def period_from(self) -> Time:
        """Get the `from` forecast period."""
        return self._from

    @property
    def period_until(self) -> Time:
        """Get the `until` forecast period."""
        return self._until

    @property
    def period_at(self) -> Optional[Time]:
        """Get the `at` forecast period."""
        return self._at

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "forecast_period": {
                "init": self.forecast_period[0].as_dict(),
                "end": self.forecast_period[1].as_dict(),
            },
            "from_": self.period_from.as_dict(),
            "until": self.period_until.as_dict(),
            "at": self.period_at.as_dict() if self.period_at else None,
        }
        d.update(super().as_dict())
        return d
