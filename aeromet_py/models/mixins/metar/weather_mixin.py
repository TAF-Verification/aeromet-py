import re

from ...metar.models import MetarWeather
from ...group import GroupList


class MetarWeatherMixin:
    """Mixin to add weather list attribute to the report."""

    def __init__(self) -> None:
        self._weathers = GroupList[MetarWeather](3)

    def _handle_weather(self, match: re.Match) -> None:
        weather: MetarWeather = MetarWeather(match)
        self._weathers.add(weather)

        self._concatenate_string(weather)

    @property
    def weathers(self) -> GroupList[MetarWeather]:
        """Get the weather data of the report if provided."""
        return self._weathers
