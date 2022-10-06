import re

from typing import Any, Dict, List, Optional

from ..utils import (
    MetarRegExp,
    TafRegExp,
    sanitize_change_indicator,
    sanitize_visibility,
    split_sentence,
)
from .models import (
    FlightRulesMixin,
    GroupHandler,
    ModifierMixin,
    ParserError,
    Report,
    Time,
    parse_section,
)
from .models.metar import (
    MetarCloudMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarWindMixin,
    ShouldBeCavokMixin,
)
from .models.taf import *


class Taf(
    Report,
    ModifierMixin,
    MetarWindMixin,
    MetarPrevailingMixin,
    MetarWeatherMixin,
    MetarCloudMixin,
    TafValidMixin,
    FlightRulesMixin,
    ShouldBeCavokMixin,
):
    """Parser for TAF reports."""

    def __init__(
        self,
        code: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
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
        MetarWindMixin.__init__(self)
        MetarPrevailingMixin.__init__(self)
        MetarWeatherMixin.__init__(self)
        MetarCloudMixin.__init__(self)
        TafValidMixin.__init__(self)
        FlightRulesMixin.__init__(self)
        ShouldBeCavokMixin.__init__(self)

        # Body groups
        self._missing = Missing(None)
        self._cancelled = Cancelled(None)
        self._max_temperatures = TafTemperatureList()
        self._min_temperatures = TafTemperatureList()

        # Change periods
        self._changes_forecasted = TafChangesForecasted()

        # Parse the body groups.
        self._parse_body()

        # Parse the change periods
        self._parse_changes_forecasted()

    @property
    def body(self) -> str:
        """Get the body part of the TAF."""
        return self._body

    @property
    def weather_changes(self) -> str:
        """Get the weather changes of the TAF."""
        return self._sections[1]

    def _handle_time(self, match: re.Match) -> None:
        self._time = Time.from_metar(match, self._year, self._month)

        self._concatenate_string(self._time)

    def _handle_missing(self, match: re.Match) -> None:
        self._missing = Missing(match.string)

        self._concatenate_string(self._missing)

    @property
    def missing(self) -> Missing:
        """Get the missing information of the TAF if provided."""
        return self._missing

    def _handle_cancelled(self, match: re.Match) -> None:
        self._cancelled = Cancelled(match)

        self._concatenate_string(self._cancelled)

    @property
    def cancelled(self) -> Cancelled:
        """Get the cancelled group data of the TAF."""
        return self._cancelled

    def _handle_temperature(self, match: re.Match) -> None:
        temperature: TafTemperature = TafTemperature(match, self._time.time)

        if match.group("type") == "X":
            self._max_temperatures.add(temperature)
        else:
            self._min_temperatures.add(temperature)

        self._concatenate_string(temperature)

    @property
    def max_temperatures(self) -> TafTemperatureList:
        """Get the maximum temperatures expected to happen."""
        return self._max_temperatures

    @property
    def min_temperatures(self) -> TafTemperatureList:
        """Get the minimum temperatures expected to happen."""
        return self._min_temperatures

    def _handle_change_forecasted(self, code: str) -> None:
        cf: ChangeForecasted = ChangeForecasted(code, self._valid)
        self._changes_forecasted.add(cf)

        self._concatenate_string(cf)

    @property
    def changes_forecasted(self) -> TafChangesForecasted:
        """Get the weather change periods data of the TAF if provided."""
        return self._changes_forecasted

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
            GroupHandler(TafRegExp.TEMPERATURE, self._handle_temperature),
            GroupHandler(TafRegExp.TEMPERATURE, self._handle_temperature),
        ]

        sanitized_body: str = sanitize_visibility(self._body)
        unparsed: List[str] = parse_section(handlers, sanitized_body)
        self._unparsed_groups += unparsed

    def _parse_changes_forecasted(self) -> None:
        for change in self._changes_codes:
            if change != "":
                self._handle_change_forecasted(change)

        for cp in self._changes_forecasted:
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

    def as_dict(self) -> Dict[str, Any]:
        d = super().as_dict()
        d.update(
            {
                "modifier": self.modifier.as_dict(),
                "missing": self.missing.as_dict(),
                "valid": self.valid.as_dict(),
                "cancelled": self.cancelled.as_dict(),
                "wind": self.wind.as_dict(),
                "prevailing_visibility": self.prevailing_visibility.as_dict(),
                "weathers": self.weathers.as_dict(),
                "clouds": self.clouds.as_dict(),
                "max_temperatures": self.max_temperatures.as_dict(),
                "min_temperatures": self.min_temperatures.as_dict(),
                "changes_forecasted": self.changes_forecasted.as_dict(),
            }
        )
        return d
