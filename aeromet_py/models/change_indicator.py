import re

from typing import Dict, List, Optional

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

    def __init__(self, match: Optional[re.Match]) -> None:
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
                    CHANGE_TRANSLATIONS[codes[0]] + " " + CHANGE_TRANSLATIONS[codes[1]]
                )
            else:
                self._translation = None

    def __str__(self) -> str:
        if self._translation:
            return self._translation

        return ""

    @property
    def translation(self) -> Optional[str]:
        """Get the translation of the change indicator."""
        return self._translation

    def as_dict(self) -> Dict[str, Optional[str]]:
        d = {"translation": self.translation}
        d.update(super().as_dict())
        return d
