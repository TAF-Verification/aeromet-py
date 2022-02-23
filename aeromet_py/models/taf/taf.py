import re
from typing import List

from ..group import GroupHandler
from ..report import Report
from ..modifier import ModifierMixin
from ...utils import split_sentence, sanitize_visibility, parse_section, MetarRegExp
from ..metar.models.time import MetarTime


class Taf(Report, ModifierMixin):
    """Parser for TAF reports."""

    def __init__(self, code: str, truncate: bool = False) -> None:
        super().__init__(code, truncate=truncate, type="TAF")
        self._body: str = ""
        self._weather_changes: List[str] = []

        self._handle_sections()

        # Initialize mixins
        ModifierMixin.__init__(self)

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

    def _parse_body(self) -> None:
        """Parse the body groups."""
        handlers: List[GroupHandler] = [
            GroupHandler(MetarRegExp.TYPE, self._handle_type),
            GroupHandler(MetarRegExp.MODIFIER, self._handle_modifier),
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
