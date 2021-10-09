import re
from collections import namedtuple
from typing import List

import aeromet_py.models as models
from aeromet_py.utils import REGEXP, sanitize_visibility, sanitize_windshear

GroupHandler = namedtuple("GroupHandler", "regex func")


class Metar(models.Report):
    """Parser for METAR code."""

    __sections = models.MetarSectionsDescriptor()

    def __init__(self, code: str, year=None, month=None, truncate=False):
        super().__init__(code)
        self.__sections = super().raw_code
        self.__year = year
        self.__month = month
        self.__truncate = truncate

        # Body models
        self.__type = models.Type("METAR")
        self.__modifier = models.Modifier(None)
        self.__time = models.Time(None)
        self.__station = models.Station(None)
        self.__wind = models.Wind(None)
        self.__wind_variation = models.WindVariation(None)
        self.__visibility = models.Visibility(None)
        self.__minimum_visibility = models.MinimumVisibility(None)
        self.__runway_range = models.RunwayRange(None)
        self.__weathers = models.Weathers()
        self.__sky = models.Sky()
        self.__temperatures = models.Temperatures(None)
        self.__pressure = models.Pressure(None)
        self.__recent_weather = models.RecentWeather(None)
        self.__windshear = models.Windshear()
        self.__sea_state = models.SeaState(None)
        self.__runway_state = models.RunwayState(None)

        # Trend models
        self.__trend = models.Trend(None)

        self.__parse_body()
        print(self.__sections)
        self.__parse_trend()

    @property
    def code(self) -> str:
        return super().raw_code

    @property
    def sections(self) -> List[str]:
        return self.__sections

    # Body handlers and its repesctive property

    def __handle_type(self, match: re.Match):
        self.__type = models.Type(match.string)

    @property
    def type(self) -> models.Type:
        return self.__type

    def __handle_station(self, match: re.Match):
        self.__station = models.Station(match.string)

    @property
    def station(self) -> models.Station:
        return self.__station

    def __handle_time(self, match: re.Match):
        self.__time = models.Time(match.string, year=self.__year, month=self.__month)

    @property
    def time(self) -> models.Time:
        return self.__time

    def __handle_modifier(self, match: re.Match):
        self.__modifier = models.Modifier(match.string)

    @property
    def modifier(self) -> models.Modifier:
        return self.__modifier

    def __handle_wind(self, match: re.Match):
        self.__wind = models.Wind(match)

    @property
    def wind(self) -> models.Wind:
        return self.__wind

    def __handle_wind_variation(self, match: re.Match):
        self.__wind_variation = models.WindVariation(match)

    @property
    def wind_variation(self) -> models.WindVariation:
        return self.__wind_variation

    def __handle_visibility(self, match: re.Match):
        self.__visibility = models.Visibility(match)

    @property
    def visibility(self) -> models.Visibility:
        return self.__visibility

    def __handle_minimum_visibility(self, match: re.Match):
        self.__minimum_visibility = models.MinimumVisibility(match)

    @property
    def minimum_visibility(self) -> models.MinimumVisibility:
        return self.__minimum_visibility

    def __handle_runway_range(self, match: re.Match):
        self.__runway_range = models.RunwayRange(match)

    @property
    def runway_range(self) -> models.RunwayRange:
        return self.__runway_range

    def __handle_weather(self, match: re.Match):
        self.__weathers.add(match)

    @property
    def weathers(self) -> models.Weathers:
        return self.__weathers

    def __handle_sky(self, match: re.Match):
        self.__sky.add(match)

    @property
    def sky(self) -> models.Sky:
        return self.__sky

    def __handle_temperatures(self, match: re.Match):
        self.__temperatures = models.Temperatures(match)

    @property
    def temperatures(self) -> models.Temperatures:
        return self.__temperatures

    def __handle_pressure(self, match: re.Match):
        self.__pressure = models.Pressure(match)

    @property
    def pressure(self) -> models.Pressure:
        return self.__pressure

    def __handle_recent_weather(self, match: re.Match):
        self.__recent_weather = models.RecentWeather(match)

    @property
    def recent_weather(self) -> models.RecentWeather:
        return self.__recent_weather

    def __handle_windshear(self, match: re.Match):
        self.__windshear.add(match)

    @property
    def windshear(self) -> models.Windshear:
        return self.__windshear

    def __handle_sea_state(self, match: re.Match):
        self.__sea_state = models.SeaState(match)

    @property
    def sea_state(self) -> models.SeaState:
        return self.__sea_state

    def __handle_runway_state(self, match: re.Match):
        self.__runway_state = models.RunwayState(match)

    @property
    def runway_state(self) -> models.RunwayState:
        return self.__runway_state

    def __handle_trend(self, match: re.Match):
        self.__trend = models.Trend(match)

    def __handle_trend_time_group(self, match: re.Match):
        period = models.Period(match)

        if period.prefix == "from":
            self.__trend.from_time = match
        elif period.prefix == "until":
            self.__trend.until_time = match
        elif period.prefix == "at":
            self.__trend.at_time = match
        else:
            return

    @property
    def trend(self) -> models.Trend:
        return self.__trend

    def __parse_body(self):
        handlers = [
            GroupHandler(REGEXP.TYPE, self.__handle_type),
            GroupHandler(REGEXP.STATION, self.__handle_station),
            GroupHandler(REGEXP.TIME, self.__handle_time),
            GroupHandler(REGEXP.MODIFIER, self.__handle_modifier),
            GroupHandler(REGEXP.WIND, self.__handle_wind),
            GroupHandler(REGEXP.WIND_VARIATION, self.__handle_wind_variation),
            GroupHandler(REGEXP.VISIBILITY, self.__handle_visibility),
            GroupHandler(REGEXP.MINIMUM_VISIBILITY, self.__handle_minimum_visibility),
            GroupHandler(REGEXP.RUNWAY_RANGE, self.__handle_runway_range),
            GroupHandler(REGEXP.WEATHER, self.__handle_weather),
            GroupHandler(REGEXP.WEATHER, self.__handle_weather),
            GroupHandler(REGEXP.WEATHER, self.__handle_weather),
            GroupHandler(REGEXP.SKY, self.__handle_sky),
            GroupHandler(REGEXP.SKY, self.__handle_sky),
            GroupHandler(REGEXP.SKY, self.__handle_sky),
            GroupHandler(REGEXP.SKY, self.__handle_sky),
            GroupHandler(REGEXP.TEMPERATURES, self.__handle_temperatures),
            GroupHandler(REGEXP.PRESSURE, self.__handle_pressure),
            GroupHandler(REGEXP.RECENT_WEATHER, self.__handle_recent_weather),
            GroupHandler(REGEXP.WINDSHEAR, self.__handle_windshear),
            GroupHandler(REGEXP.WINDSHEAR, self.__handle_windshear),
            GroupHandler(REGEXP.WINDSHEAR, self.__handle_windshear),
            GroupHandler(REGEXP.SEA_STATE, self.__handle_sea_state),
            GroupHandler(REGEXP.RUNWAY_STATE, self.__handle_runway_state),
        ]

        self._parse(handlers, self.__sections[0])

    def __parse_trend(self):
        handlers = [
            GroupHandler(REGEXP.TREND, self.__handle_trend),
            GroupHandler(REGEXP.TREND_TIME_GROUP, self.__handle_trend_time_group),
            GroupHandler(REGEXP.TREND_TIME_GROUP, self.__handle_trend_time_group),
        ]

        self._parse(handlers, self.__sections[1], section_type="trend")

    def _parse(
        self, handlers: List[GroupHandler], section: str, section_type: str = "body"
    ) -> None:
        """Parse the groups of section_type.

        Args:
            handlers (List[GroupHandler]): handler list to manage and match.
            section (str): the section containing all the groups to parse.
            section_type (str, optional): the section type to parse. Defaults to "body".

        Raises:
            models.ParserError: if self.unparser_groups has items and self.__truncate == True,
            raises the error.
        """
        index = 0
        section = sanitize_visibility(section)
        if section_type == "body":
            section = sanitize_windshear(section)

        for group in section.split(" "):
            self.unparsed_groups.append(group)

            for handler in handlers[index:]:
                match = re.match(handler.regex, group)
                index += 1
                if match:
                    handler.func(match)
                    self.unparsed_groups.remove(group)
                    break

        if self.unparsed_groups and self.__truncate:
            raise models.ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )
