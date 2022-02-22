import re
from typing import List

from ..report import Report
from ...utils import split_sentence, sanitize_visibility, parse_section
from ..metar.models.time import MetarTime


class Taf(Report):
    """Parser for TAF reports."""

    def __init__(self, code: str, truncate: bool = False) -> None:
        super().__init__(code, truncate)
        self._body: str = ""
        self._weather_changes: List[str] = []

        self._handle_sections()

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

    def _handle_sections(self) -> None:
        keywords: List[str] = ["FM", "TEMPO", "BECMG", "PROB"]
        sections: List[str] = split_sentence(self._raw_code, keywords, space="left")

        self._body = sections[0]
        if len(sections) > 1:
            self._weather_changes = sections[1:]

        self._sections = [self._body, " ".join(self._weather_changes)]
