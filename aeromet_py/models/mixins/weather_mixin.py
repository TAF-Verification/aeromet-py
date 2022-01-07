import re

from ..weather import Weather
from ..group import GroupList


class WeatherMixin:
    """Mixin to add weather list attribute to the report."""

    def __init__(self) -> None:
        self._weathers = GroupList[Weather](3)

    def _handle_weather(self, match: re.Match) -> None:
        _weather: Weather = Weather(match)
        self._weathers.add(_weather)

        self._concatenate_string(_weather)

    @property
    def weathers(self) -> GroupList[Weather]:
        """Returns the weather data of the report.

        Returns:
            GroupList[Weather]: the list of Weather class instance.
        """
        return self._weathers
