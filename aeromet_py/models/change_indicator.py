import re
from typing import Dict, List

from .group import Group

CHANGE_TRANSLATIONS: Dict[str, str] = {
    "NOSIG": "no significant changes",
    "BECMG": "becoming",
    "TEMPO": "temporary",
    "PROB30": "probability 30%",
    "PROB40": "probability 40%",
}


class ChangeIndicator(Group):
    """Basic structure for trend codes in the report."""

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._translation = None
        else:
            super().__init__(match.string)

            if match.string in CHANGE_TRANSLATIONS.keys():
                self._translation = CHANGE_TRANSLATIONS[match.string]
            elif match.string.startswith("PROB"):
                codes: List[str] = match.string.split("_")
                self._translation = (
                    CHANGE_TRANSLATIONS[codes[0]] + CHANGE_TRANSLATIONS[codes[1]]
                )
            else:
                self._translation = None

    def __str__(self) -> str:
        if self._translation:
            return self._translation

        return ""

    @property
    def translation(self) -> str:
        """Get the translation of the change indicator."""
        return self._translation