import re
from collections import namedtuple
from typing import List

from aeromet_py.models.metar.models.pressure import MetarPressure
from aeromet_py.utils import MetarRegExp, sanitize_visibility, sanitize_windshear

from ..errors import ParserError
from ..group import GroupList
from ..mixins import (
    MetarCloudMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarWindMixin,
    ModifierMixin,
)
from ..report import Report
from .models import *

GroupHandler = namedtuple("GroupHandler", "regexp handler")


class Metar(
    Report,
    ModifierMixin,
    MetarWindMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarCloudMixin,
):
    """Parser for METAR reports."""

    def __init__(
        self, code: str, year: int = None, month: int = None, truncate: bool = False
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

        # Groups
        self._wind_variation = MetarWindVariation(None)
        self._minimum_visibility = MetarMinimumVisibility(None)
        self._runway_ranges = GroupList[MetarRunwayRange](3)
        self._temperatures = MetarTemperatures(None)
        self._pressure = MetarPressure(None)
        self._recent_weather = MetarRecentWeather(None)
        self._windshear = MetarWindshearList()
        self._sea_state = MetarSeaState(None)
        self._runway_state = MetarRunwayState(None)

        # Parse groups
        self._parse_body()

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
        self._time = MetarTime(match, self._year, self._month)

        self._concatenate_string(self._time)

    @property
    def time(self) -> MetarTime:
        """Get the time of the report."""
        return self._time

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
        self._windshear.add(windshear)

        self._concatenate_string(windshear)

    @property
    def windshear(self) -> MetarWindshearList:
        """Get the windshear data of the METAR."""
        return self._windshear

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

    def _parse_body(self) -> None:
        handlers = [
            GroupHandler(MetarRegExp.TYPE, self._handle_type),
            GroupHandler(MetarRegExp.STATION, self._handle_station),
            GroupHandler(MetarRegExp.TIME, self._handle_time),
            GroupHandler(MetarRegExp.MODIFIER, self._handle_modifier),
            GroupHandler(MetarRegExp.WIND, self._handle_wind),
            GroupHandler(MetarRegExp.WIND_VARIATION, self._handle_wind_variation),
            GroupHandler(MetarRegExp.VISIBILITY, self._handle_prevailing),
            GroupHandler(MetarRegExp.VISIBILITY, self._handle_minimum_visibility),
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
            GroupHandler(MetarRegExp.RECENT_WEATHER, self._handle_recent_weather),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.WINDSHEAR, self._handle_windshear),
            GroupHandler(MetarRegExp.SEA_STATE, self._handle_sea_state),
            GroupHandler(MetarRegExp.RUNWAY_STATE, self._handle_runway_state),
        ]

        self._parse(handlers, self.body)

    def _parse(
        self, handlers: List[GroupHandler], section: str, section_type: str = "body"
    ) -> None:
        """Parse the groups of section_type.
        Args:
            handlers (List[GroupHandler]): handler list to manage and match.
            section (str): the section containing all the groups to parse.
            section_type (str, optional): the section type to parse. Defaults to "body".
                Options: body, trend, remark.
        Raises:
            ParserError: if self.unparser_groups has items and self.__truncate == True,
            raises the error.
        """
        index = 0
        section = sanitize_visibility(section)
        if section_type == "body":
            section = sanitize_windshear(section)

        for group in section.split(" "):
            self.unparsed_groups.append(group)

            for group_handler in handlers[index:]:
                match = re.match(group_handler.regexp, group)
                index += 1
                if match:
                    group_handler.handler(match)
                    self.unparsed_groups.remove(group)
                    break

        if self.unparsed_groups and self._truncate:
            raise ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )

    def _handle_sections(self) -> None:
        trend_re: re.Pattern = re.compile(
            MetarRegExp.TREND.replace("^", "").replace("$", "")
        )
        remark_re: re.Pattern = re.compile(
            MetarRegExp.REMARK.replace("^", "").replace("$", "")
        )

        trend_pos: int = None
        remark_pos: int = None

        try:
            trend_pos = trend_re.search(self._raw_code).start()
        except AttributeError:
            pass

        try:
            remark_pos = remark_re.search(self._raw_code).start()
        except AttributeError:
            pass

        body: str = ""
        trend: str = ""
        remark: str = ""

        if trend_pos is None and remark_pos is not None:
            body = self._raw_code[: remark_pos - 1]
            remark = self._raw_code[remark_pos:]
        elif trend_pos is not None and remark_pos is None:
            body = self._raw_code[: trend_pos - 1]
            trend = self._raw_code[trend_pos:]
        elif trend_pos is None and remark_pos is None:
            body = self._raw_code
        else:
            if trend_pos > remark_pos:
                body = self._raw_code[: remark_pos - 1]
                remark = self._raw_code[remark_pos : trend_pos - 1]
                trend = self._raw_code[trend_pos:]
            else:
                body = self._raw_code[: trend_pos - 1]
                trend = self._raw_code[trend_pos : remark_pos - 1]
                remark = self._raw_code[remark_pos:]

        self._sections = [body, trend, remark]
