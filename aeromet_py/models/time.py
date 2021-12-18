from datetime import datetime
from typing import Tuple

from .descriptor import DataDescriptor
from .group import Group


class Time(Group):
    """Basic structure for time groups in reports from land stations."""

    _time = DataDescriptor()

    def __init__(self, original_code: str, generated_code: str) -> None:
        super().__init__(original_code)

        if generated_code is not None:
            self._time = datetime.strptime(generated_code, "%Y%m%d%H%MZ")

    def _verify_none(self, year: int, month: int) -> Tuple[int, int, datetime]:
        """Verify if year or month are None. In case of some of them
        are None, it is reassigned to current year or month.

        Args:
            year (int): the year.
            month (int): the month.

        Returns:
            Tuple[int, int, datetime]: year, month verified and not None, and the
            current date as a datetime object.
        """
        date = datetime.utcnow()
        if year is None:
            year = date.year
        if month is None:
            month = date.month

        return year, month, date

    @classmethod
    def from_METAR(
        cls, original_code: str, year: int = None, month: int = None
    ) -> "Time":
        """Classmethod to create a Time object from a METAR time group.

        Returns:
            Time: the Time object.
        """
        year, month, date = cls._verify_none(cls, year, month)

        if original_code is None:
            original_code = "{:02d}{:02d}{:02d}Z".format(
                date.day,
                date.hour,
                date.minute,
            )

        generated_code: str = "{:4d}{:02d}{}".format(
            year,
            month,
            original_code,
        )

        obj: "Time" = cls(original_code, generated_code)

        return obj

    def __str__(self) -> str:
        return str(self._time)

    @property
    def time(self) -> datetime:
        """Returns the time of the report.

        Returns:
            datetime: the time as a datetime object.
        """
        return self._time

    @property
    def year(self) -> int:
        """Returns the year of the report.

        Returns:
            int: the year.
        """
        return self._time.year

    @property
    def month(self) -> int:
        """Returns the month of the report.

        Returns:
            int: the month.
        """
        return self._time.month

    @property
    def day(self) -> int:
        """Returns the day of the report.

        Returns:
            int: the day.
        """
        return self._time.day

    @property
    def hour(self) -> int:
        """Returns the UTC hour of the report.

        Returns:
            int: the hour.
        """
        return self._time.hour

    @property
    def minute(self) -> int:
        """Returns the minute of the report.

        Returns:
            int: the minute.
        """
        return self._time.minute
