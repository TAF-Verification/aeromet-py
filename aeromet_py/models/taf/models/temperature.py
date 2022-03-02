import re
from datetime import datetime, timedelta

from ...group import Group
from ...temperature import Temperature
from ...time import Time


class TafTemperature(Temperature, Group):
    """Basic structure for temperature groups in TAF."""

    def __init__(self, match: re.Match, time: datetime) -> None:
        time = time.replace(minute=0)

        if match is None:
            super().__init__(None)
            Group.__init__(self, None)

            self._time = None
        else:
            Group.__init__(self, match.string)

            _sign: str = match.group("sign")
            _temp: str = match.group("temp")

            if _sign:
                super().__init__("-" + _temp)
            else:
                super().__init__(_temp)

            _day: int = int(match.group("day"))
            _hour: int = int(match.group("hour"))

            time = time.replace(hour=_hour)
            if _day == time.day:
                self._time = Time(time=time)
            else:
                time = time + timedelta(days=1)
                self._time = Time(time=time)

    def __str__(self) -> str:
        if self._value is None:
            return super().__str__()

        return super().__str__() + f" at {self._time}"

    @property
    def time(self) -> Time:
        """Get the date and time the temperature is expected to happen."""
        return self._time
