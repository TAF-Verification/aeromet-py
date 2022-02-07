import re
from typing import Dict

from .group import Group

TREND_TRANSLATIONS: Dict[str, str] = {
    "NOSIG": "no significant changes",
    "BECMG": "becoming",
    "TEMPO": "temporary",
    "PROB30": "probability 30%",
    "PROB40": "probability 40%",
}


class Trend(Group):
    """Basic structure for trend codes in the report."""

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._translation = None
        else:
            super().__init__(match.group("trend"))

            self._translation = TREND_TRANSLATIONS.get(match.group("trend"), None)

    def __str__(self) -> str:
        if self._translation:
            return self._translation

        return ""

    @property
    def translation(self) -> str:
        """Get the translation of the trend."""
        return self._translation
