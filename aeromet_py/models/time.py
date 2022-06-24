from datetime import datetime
from typing import Dict, Optional
import re


class Time:
    """Basic structure for time code groups in reports from land stations."""

    def __init__(
        self,
        minute: Optional[str] = None,
        hour: Optional[str] = None,
        day: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        time: Optional[datetime] = None,
    ) -> None:
        self._time: datetime

        if time:
            self._time = time
        else:
            today: datetime = datetime.utcnow()

            if year is None:
                year = today.year

            if month is None:
                month = today.month

            if day is None:
                day = "01"

            if hour is None:
                hour = "00"

            if minute is None:
                minute = "00"

            generated_date: str = "{}{:02d}{}{}{}".format(
                year,
                month,
                day,
                hour,
                minute,
            )
            self._time = datetime.strptime(generated_date, "%Y%m%d%H%M")

    @classmethod
    def from_metar(
        cls,
        match: Optional[re.Match],
        year: Optional[int] = None,
        month: Optional[int] = None,
    ) -> "Time":
        if match is None:
            return cls()
        else:
            minute = match.group("min")
            day = match.group("day")
            hour = match.group("hour")

            return cls(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                year=year,
            )

    def __str__(self) -> str:
        return str(self._time)

    @property
    def time(self) -> datetime:
        """Get the time of the report as a `datetime` object."""
        return self._time

    @property
    def year(self) -> int:
        """Get the year of the report."""
        return self._time.year

    @property
    def month(self) -> int:
        """Get the month of the report."""
        return self._time.month

    @property
    def day(self) -> int:
        """Get the day of the report."""
        return self._time.day

    @property
    def hour(self) -> int:
        """Get the hour of the report."""
        return self._time.hour

    @property
    def minute(self) -> int:
        """Get the minute of the report."""
        return self._time.minute

    def to_dict(self) -> Dict[str, str]:
        return {
            "datetime": str(self.time),
        }


class TimeMixin:
    """Basic structure to add `Time` attribute to the report or section."""

    def __init__(self) -> None:
        self._time: Time = Time()
