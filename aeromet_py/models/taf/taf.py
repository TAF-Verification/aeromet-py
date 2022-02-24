import re
from typing import List

from aeromet_py.utils.taf_regexp import TafRegExp

from ...utils import MetarRegExp, parse_section, sanitize_visibility, split_sentence
from ..group import GroupHandler
from ..metar.models.time import MetarTime
from ..modifier import ModifierMixin
from ..report import Report
from .models import *


class Taf(Report, ModifierMixin):
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

        # Body groups
        self._missing = Missing(None)

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

    def _parse_body(self) -> None:
        """Parse the body groups."""
        handlers: List[GroupHandler] = [
            GroupHandler(MetarRegExp.TYPE, self._handle_type),
            GroupHandler(TafRegExp.AMD_COR, self._handle_modifier),
            GroupHandler(MetarRegExp.STATION, self._handle_station),
            GroupHandler(MetarRegExp.TIME, self._handle_time),
            GroupHandler(TafRegExp.NIL, self._handle_missing),
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
