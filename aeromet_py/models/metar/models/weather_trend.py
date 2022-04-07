import re
from datetime import datetime
from typing import List

from ....utils import MetarRegExp, parse_section, sanitize_visibility
from ...cloud import MetarCloudMixin
from ...flight_rules import FlightRulesMixin
from ...group import Group, GroupHandler, GroupList
from ...string_attribute import StringAttributeMixin
from ...time import Time
from .trend_indicator import MetarTrendIndicator
from .visibility import MetarPrevailingMixin
from .weather import MetarWeatherMixin
from .wind import MetarWindMixin


class Forecast(
    Group,
    StringAttributeMixin,
    MetarWindMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarCloudMixin,
    FlightRulesMixin,
):
    """Basic structure for change periods and forecasts in METAR and TAF respectively."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self._unparsed_groups: List[str] = []

        # Initialize mixins
        StringAttributeMixin.__init__(self)
        MetarWindMixin.__init__(self)
        MetarPrevailingMixin.__init__(self)
        MetarWeatherMixin.__init__(self)
        MetarCloudMixin.__init__(self)
        FlightRulesMixin.__init__(self)

    def __str__(self) -> str:
        return StringAttributeMixin.__str__(self)

    @property
    def unparsed_groups(self) -> List[str]:
        """Get the unparsed groups of the change period."""
        return self._unparsed_groups


class ChangePeriod(Forecast):
    """Basic structure for change period of trend in METAR."""

    def __init__(self, code: str, time: datetime) -> None:
        super().__init__(code)

        self._time: Time = Time(time=time)

        # Groups
        self._change_indicator = MetarTrendIndicator(None, time)

        # Parse the groups
        self._parse()

    def _handle_change_indicator(self, match: re.Match) -> None:
        self._change_indicator = MetarTrendIndicator(match, self._time.time)

        self._concatenate_string(self._change_indicator)

    @property
    def change_indicator(self) -> MetarTrendIndicator:
        """Get the trend indicator data of the METAR."""
        return self._change_indicator

    def _handle_time_period(self, match: re.Match) -> None:
        old_change_indicator = str(self._change_indicator)
        self._change_indicator.add_period(match)
        new_change_indicator = str(self._change_indicator)

        self._string = self._string.replace(old_change_indicator, new_change_indicator)

    def _parse(self) -> None:
        handlers: List[GroupHandler] = [
            GroupHandler(MetarRegExp.CHANGE_INDICATOR, self._handle_change_indicator),
            GroupHandler(MetarRegExp.TREND_TIME_PERIOD, self._handle_time_period),
            GroupHandler(MetarRegExp.TREND_TIME_PERIOD, self._handle_time_period),
            GroupHandler(MetarRegExp.WIND, self._handle_wind),
            GroupHandler(MetarRegExp.VISIBILITY, self._handle_prevailing),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
        ]

        sanitized_code = sanitize_visibility(self._code)
        unparsed: List[str] = parse_section(handlers, sanitized_code)
        self._unparsed_groups += unparsed


class MetarWeatherTrends(GroupList[ChangePeriod]):
    """Basic structure for weather trends sections in METAR."""

    def __init__(self) -> None:
        super().__init__(2)

    def __str__(self) -> str:
        return "\n".join(str(change) for change in self._list)
