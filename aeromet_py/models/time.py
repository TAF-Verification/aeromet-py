from datetime import datetime

from .descriptors import CodeDescriptor, DataDescriptor


class TimeDescriptor(DataDescriptor):
    """Time descriptor. Creates a datetime object as its data."""

    def _handler(self, value):
        return datetime.strptime(value, "%Y%m%d%H%MZ")


class Time:
    """The time of the report (class)."""

    __code = CodeDescriptor()
    __time = TimeDescriptor()

    def __init__(self, code: str, month=None, year=None):
        date = datetime.utcnow()
        if year is None:
            year = date.year
        if month is None:
            month = date.month

        if code is None:
            code = "{:02d}{:02d}{:02d}Z".format(
                date.day,
                date.hour,
                date.minute,
            )

        self.__code = code
        self.__group = "{:4d}{:02d}{}".format(
            year,
            month,
            self.__code,
        )
        self.__time = self.__group

    @property
    def code(self) -> str:
        """Returns the time code of the report if present."""
        return self.__code

    @property
    def time(self) -> datetime:
        """Returns the time of the report as a datetime object."""
        return self.__time

    def __str__(self) -> str:
        return str(self.__time)
