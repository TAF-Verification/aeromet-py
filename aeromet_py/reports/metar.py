import re

from typing import Any, Dict, List, Optional

from ..utils import MetarRegExp, sanitize_visibility, sanitize_windshear, split_sentence
from .models import (
    FlightRulesMixin,
    GroupHandler,
    GroupList,
    ModifierMixin,
    ParserError,
    Report,
    Time,
    parse_section,
)
from .models.metar import *


class Metar(
    Report,
    ModifierMixin,
    MetarWindMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarCloudMixin,
    FlightRulesMixin,
    ShouldBeCavokMixin,
):
    """Parser for METAR reports."""

    def __init__(
        self,
        code: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        truncate: bool = False,
    ) -> None:
        super().__init__(code, truncate)
        self._year = year
        self._month = month

        self._handle_sections()

        # Initialize mixins
        ModifierMixin.__init__(self)
        MetarWindMixin.__init__(self)
        MetarPrevailingMixin.__init__(self)
        MetarWeatherMixin.__init__(self)
        MetarCloudMixin.__init__(self)
        FlightRulesMixin.__init__(self)
        ShouldBeCavokMixin.__init__(self)

        # Body groups
        self._time = Time.from_metar(year=year, month=month)
        self._wind_variation = MetarWindVariation(None)
        self._minimum_visibility = MetarMinimumVisibility(None)
        self._runway_ranges = GroupList[MetarRunwayRange](3)
        self._temperatures = MetarTemperatures(None)
        self._pressure = MetarPressure(None)
        self._recent_weather = MetarRecentWeather(None)
        self._windshears = MetarWindshearList()
        self._sea_state = MetarSeaState(None)
        self._runway_state = MetarRunwayState(None)

        # Trend groups
        self._weather_trends = MetarWeatherTrends()

        # Parse groups
        self._parse_body()
        self._parse_weather_trend()

    @property
    def body(self) -> str:
        """Get the body part of the METAR."""
        return self._sections[0]

    @property
    def trend(self) -> str:
        """Get the trend part of the METAR."""
        return self._sections[1]

    @property
    def remark(self) -> str:
        """Get the remark part of the METAR."""
        return self._sections[2]

    def _handle_time(self, match: re.Match) -> None:
        self._time = Time.from_metar(match, self._year, self._month)

        self._concatenate_string(self._time)

    def _handle_wind_variation(self, match: re.Match) -> None:
        self._wind_variation = MetarWindVariation(match)

        self._concatenate_string(self._wind_variation)

    @property
    def wind_variation(self) -> MetarWindVariation:
        """Get the wind variation directions from the METAR."""
        return self._wind_variation

    def _handle_minimum_visibility(self, match: re.Match) -> None:
        self._minimum_visibility = MetarMinimumVisibility(match)

        self._concatenate_string(self._minimum_visibility)

    @property
    def minimum_visibility(self) -> MetarMinimumVisibility:
        """Get the minimum visibility data of the METAR."""
        return self._minimum_visibility

    def _handle_runway_range(self, match: re.Match) -> None:
        range: MetarRunwayRange = MetarRunwayRange(match)
        self._runway_ranges.add(range)

        self._concatenate_string(range)

    @property
    def runway_ranges(self) -> GroupList[MetarRunwayRange]:
        """Get the runway ranges data of the METAR if provided."""
        return self._runway_ranges

    def _handle_temperatures(self, match: re.Match) -> None:
        self._temperatures = MetarTemperatures(match)

        self._concatenate_string(self._temperatures)

    @property
    def temperatures(self) -> MetarTemperatures:
        """Get the temperatures data of the METAR."""
        return self._temperatures

    def _handle_pressure(self, match: re.Match) -> None:
        self._pressure = MetarPressure(match)

        self._concatenate_string(self._pressure)

    @property
    def pressure(self) -> MetarPressure:
        """Get the pressure of the METAR."""
        return self._pressure

    def _handle_recent_weather(self, match: re.Match) -> None:
        self._recent_weather = MetarRecentWeather(match)

        self._concatenate_string(self._recent_weather)

    @property
    def recent_weather(self) -> MetarRecentWeather:
        """Get the recent weather data of the METAR."""
        return self._recent_weather

    def _handle_windshear(self, match: re.Match) -> None:
        windshear: MetarWindshearRunway = MetarWindshearRunway(match)
        self._windshears.add(windshear)

        self._concatenate_string(windshear)

    @property
    def windshears(self) -> MetarWindshearList:
        """Get the windshear data of the METAR."""
        return self._windshears

    def _handle_sea_state(self, match: re.Match) -> None:
        self._sea_state = MetarSeaState(match)

        self._concatenate_string(self._sea_state)

    @property
    def sea_state(self) -> MetarSeaState:
        """Get the sea state data of the METAR."""
        return self._sea_state

    def _handle_runway_state(self, match: re.Match) -> None:
        self._runway_state = MetarRunwayState(match)

        self._concatenate_string(self._runway_state)

    @property
    def runway_state(self) -> MetarRunwayState:
        """Get the runway state data of the METAR."""
        return self._runway_state

    def _handle_weather_trend(self, code: str) -> None:
        wt: ChangePeriod = ChangePeriod(code, self._time.time)
        self._weather_trends.add(wt)

        self._concatenate_string(wt)

    @property
    def weather_trends(self) -> MetarWeatherTrends:
        """Get the weather trends of the METAR if provided."""
        return self._weather_trends

    def _parse_body(self) -> None:
        """Parse the body section."""

        handlers: List[GroupHandler] = [
            GroupHandler(MetarRegExp.TYPE, self._handle_type),
            GroupHandler(MetarRegExp.STATION, self._handle_station),
            GroupHandler(MetarRegExp.TIME, self._handle_time),
            GroupHandler(MetarRegExp.MODIFIER, self._handle_modifier),
            GroupHandler(MetarRegExp.WIND, self._handle_wind),
            GroupHandler(MetarRegExp.WIND_VARIATION, self._handle_wind_variation),
            GroupHandler(MetarRegExp.VISIBILITY, self._handle_prevailing),
            GroupHandler(
                MetarRegExp.MINIMUM_VISIBILITY, self._handle_minimum_visibility
            ),
            GroupHandler(MetarRegExp.RUNWAY_RANGE, self._handle_runway_range),
            GroupHandler(MetarRegExp.RUNWAY_RANGE, self._handle_runway_range),
            GroupHandler(MetarRegExp.RUNWAY_RANGE, self._handle_runway_range),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.TEMPERATURES, self._handle_temperatures),
            GroupHandler(MetarRegExp.PRESSURE, self._handle_pressure),
            GroupHandler(MetarRegExp.PRESSURE, self._handle_pressure),
            GroupHandler(MetarRegExp.RECENT_WEATHER, self._handle_recent_weather),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.SEA_STATE, self._handle_sea_state),
            GroupHandler(MetarRegExp.RUNWAY_STATE, self._handle_runway_state),
        ]

        sanitized_body: str = sanitize_visibility(self.body)
        sanitized_body = sanitize_windshear(sanitized_body)

        unparsed: List[str] = parse_section(handlers, sanitized_body)
        self._unparsed_groups += unparsed

    def _parse_weather_trend(self) -> None:
        """Parse the weather trend section.

        Raises:
            ParserError: if self.unparser_groups has items and self._truncate is True,
            raises the error.
        """
        _trends: List[str] = split_sentence(
            self.trend,
            ["TEMPO", "BECMG"],
            space="both",
            count=1,
        )

        for trend in _trends:
            if trend != "":
                self._handle_weather_trend(trend)

        for wt in self._weather_trends:
            self._unparsed_groups += wt.unparsed_groups

        if self.unparsed_groups and self._truncate:
            raise ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )

    def _handle_sections(self) -> None:
        sections: List[str] = split_sentence(
            self._raw_code, ["NOSIG", "TEMPO", "BECMG", "RMK"], space="left"
        )

        trend: str = ""
        remark: str = ""
        body: str = ""
        for section in sections:
            if (
                section.startswith("TEMPO")
                or section.startswith("BECMG")
                or section.startswith("NOSIG")
            ):
                trend += section + " "
            elif section.startswith("RMK"):
                remark = section
            else:
                body = section

        self._sections = [body, trend.strip(), remark]

    def as_dict(self) -> Dict[str, Any]:
        d = super().as_dict()
        d.update(
            {
                "modifier": self.modifier.as_dict(),
                "wind": self.wind.as_dict(),
                "wind_variation": self.wind_variation.as_dict(),
                "prevailing_visibility": self.prevailing_visibility.as_dict(),
                "minimum_visibility": self.minimum_visibility.as_dict(),
                "runway_ranges": self.runway_ranges.as_dict(),
                "weathers": self.weathers.as_dict(),
                "clouds": self.clouds.as_dict(),
                "temperatures": self.temperatures.as_dict(),
                "pressure": self.pressure.as_dict(),
                "recent_weather": self.recent_weather.as_dict(),
                "windshears": self.windshears.as_dict(),
                "sea_state": self.sea_state.as_dict(),
                "runway_state": self.runway_state.as_dict(),
                "flight_rules": self.flight_rules,
                "weather_trends": self.weather_trends.as_dict(),
                "remark": self.remark,
            }
        )
        return d
