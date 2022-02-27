import re
from typing import List

from ...utils import (
    MetarRegExp,
    TafRegExp,
    parse_section,
    sanitize_visibility,
    split_sentence,
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
        self._weather_changes: List[str] = []
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
        TafValidMixin.__init__(self, self._time.time)

        # Body groups
        self._missing = Missing(None)
        self._cancelled = Cancelled(None)

        # Parse the body groups.
        self._parse_body()

    @property
    def body(self) -> str:
        """Get the body part of the TAF."""
        return self._body

    @property
    def weather_changes(self) -> str:
        """Get the weather changes of the TAF."""
        if len(self._weather_changes) > 0:
            return " ".join(self._weather_changes)

        return ""

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
        ]

        unparsed: List[str] = parse_section(handlers, self._body)
        self._unparsed_groups += unparsed

    def _handle_sections(self) -> None:
        keywords: List[str] = ["FM", "TEMPO", "BECMG", "PROB"]
        sections: List[str] = split_sentence(self._raw_code, keywords, space="left")

        self._body = sections[0]
        if len(sections) > 1:
            self._weather_changes = sections[1:]

        self._sections = [self._body, " ".join(self._weather_changes)]
