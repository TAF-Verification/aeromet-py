from datetime import datetime
from typing import Union


class Time:
    """Basic structure for time code groups in reports from land stations."""

    def __init__(
        self,
        day: str = None,
        hour: str = None,
        minute: str = None,
        year: int = None,
        month: int = None,
        time: datetime = None,
    ) -> None:
        if time:
            self._time = time
        else:
            today: datetime = datetime.utcnow()

            if year is None:
                year = today.year

            if month is None:
                month = today.month

            if day is None:
                day = f"{today.day:02d}"

            if hour is None:
                hour = f"{today.hour:02d}"

            if minute is None:
                minute = f"{today.minute:02d}"

            self._time: datetime
            generated_date: str = "{}{:02d}{}{}{}".format(
                year,
                month,
                day,
                hour,
                minute,
            )
            self._time = datetime.strptime(generated_date, "%Y%m%d%H%M")

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


class TimeMixin:
    """Basic structure to add `Time` attribute to the report or section."""

    def __init__(self) -> None:
        self._time: Time = Time()
