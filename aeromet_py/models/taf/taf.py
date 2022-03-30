import re
from typing import List

from ..errors import ParserError
from ...utils import (
    MetarRegExp,
    TafRegExp,
    parse_section,
    sanitize_visibility,
    split_sentence,
    sanitize_change_indicator,
)
from ..cloud import MetarCloudMixin
from ..group import GroupHandler
from ..metar.models import (
    MetarPrevailingMixin,
    MetarTime,
    MetarTimeMixin,
    MetarWeatherMixin,
    MetarWindMixin,
)
from ..modifier import ModifierMixin
from ..report import Report
from .models import *


class Taf(
    Report,
    ModifierMixin,
    MetarTimeMixin,
    MetarWindMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarCloudMixin,
    TafValidMixin,
):
    """Parser for TAF reports."""

    def __init__(
        self,
        code: str,
        year: int = None,
        month: int = None,
        truncate: bool = False,
    ) -> None:
        super().__init__(code, truncate=truncate, type="TAF")
        self._body: str = ""
        self._changes_codes: List[str] = []
        self._year = year
        self._month = month

        self._handle_sections()

        # Initialize mixins
        ModifierMixin.__init__(self)
        MetarTimeMixin.__init__(self)
        MetarWindMixin.__init__(self)
        MetarPrevailingMixin.__init__(self)
        MetarWeatherMixin.__init__(self)
        MetarCloudMixin.__init__(self)
        TafValidMixin.__init__(self)

        # Body groups
        self._missing = Missing(None)
        self._cancelled = Cancelled(None)
        self._max_temperature = TafTemperature(None, self._time.time)
        self._min_temperature = TafTemperature(None, self._time.time)

        # Change periods
        self._change_periods = TafChangePeriods()

        # Parse the body groups.
        self._parse_body()

        # Parse the change periods
        self._parse_change_periods()

    @property
    def body(self) -> str:
        """Get the body part of the TAF."""
        return self._body

    @property
    def weather_changes(self) -> str:
        """Get the weather changes of the TAF."""
        return self._sections[1]

    def _handle_time(self, match: re.Match) -> None:
        self._time = MetarTime(match, self._year, self._month)

        self._concatenate_string(self._time)

    @property
    def time(self) -> MetarTime:
        """Get the time of the report."""
        return self._time

    def _handle_missing(self, match: re.Match) -> None:
        self._missing = Missing(match.string)

        self._concatenate_string(self._missing)

    @property
    def missing(self) -> Missing:
        """Get the missing data of the TAF."""
        return self._missing

    def _handle_cancelled(self, match: re.Match) -> None:
        self._cancelled = Cancelled(match)

        self._concatenate_string(self._cancelled)

    @property
    def cancelled(self) -> Cancelled:
        """Get the cancelled group data of the TAF."""
        return self._cancelled

    def _handle_temperature(self, match: re.Match) -> None:
        if match.group("type") == "X":
            self._max_temperature = TafTemperature(match, self._time.time)

            self._concatenate_string(self._max_temperature)
        else:
            self._min_temperature = TafTemperature(match, self._time.time)

            self._concatenate_string(self._min_temperature)

    @property
    def max_temperature(self) -> TafTemperature:
        """Get the maximum temperature expected to happen."""
        return self._max_temperature

    @property
    def min_temperature(self) -> TafTemperature:
        """Get the minimum temperature expected to happen."""
        return self._min_temperature

    def _handle_change_period(self, code: str) -> None:
        cf: ChangeForecast = ChangeForecast(code, self._valid)
        self._change_periods.add(cf)

        self._concatenate_string(cf)

    @property
    def change_periods(self) -> TafChangePeriods:
        """Get the weather change periods data of the TAF if provided."""
        return self._change_periods

    def _parse_body(self) -> None:
        """Parse the body groups."""
        handlers: List[GroupHandler] = [
            GroupHandler(MetarRegExp.TYPE, self._handle_type),
            GroupHandler(TafRegExp.AMD_COR, self._handle_modifier),
            GroupHandler(MetarRegExp.STATION, self._handle_station),
            GroupHandler(MetarRegExp.TIME, self._handle_time),
            GroupHandler(TafRegExp.NIL, self._handle_missing),
            GroupHandler(TafRegExp.VALID, self._handle_valid_period),
            GroupHandler(TafRegExp.CANCELLED, self._handle_cancelled),
            GroupHandler(TafRegExp.WIND, self._handle_wind),
            GroupHandler(TafRegExp.VISIBILITY, self._handle_prevailing),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(TafRegExp.TEMPERATURE, self._handle_temperature),
            GroupHandler(TafRegExp.TEMPERATURE, self._handle_temperature),
        ]

        sanitized_body: str = sanitize_visibility(self._body)
        unparsed: List[str] = parse_section(handlers, sanitized_body)
        self._unparsed_groups += unparsed

    def _parse_change_periods(self) -> None:
        for change in self._changes_codes:
            if change != "":
                self._handle_change_period(change)

        for cp in self._change_periods:
            self._unparsed_groups += cp.unparsed_groups

        if self.unparsed_groups and self._truncate:
            raise ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )

    def _handle_sections(self) -> None:
        keywords: List[str] = ["FM", "TEMPO", "BECMG", "PROB"]
        sanitized_code: str = sanitize_change_indicator(self._raw_code)
        if sanitized_code.startswith("TAF"):
            sanitized_code = sanitized_code.replace("TAF ", "TAF_")
        sections: List[str] = split_sentence(sanitized_code, keywords, space="left")
        sections[0] = sections[0].replace("TAF_", "TAF ")

        self._body = sections[0]
        if len(sections) > 1:
            self._changes_codes = [section for section in sections[1:]]

        self._sections = [
            self._body,
            " ".join(change.replace("_", " ") for change in self._changes_codes),
        ]
