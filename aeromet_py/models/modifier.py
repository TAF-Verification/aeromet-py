import re
from typing import Dict, Optional

from .group import Group

MODIFIERS: Dict[str, str] = {
    "COR": "Correction",
    "CORR": "Correction",
    "AMD": "Amendment",
    "NIL": "Missing report",
    "AUTO": "Automatic report",
    "TEST": "Testing report",
    "FINO": "Missing report",
}


class Modifier(Group):
    """Basic structure for modifier groups in reports from land stations."""

    def __init__(self, code: Optional[str]) -> None:
        super().__init__(code)
        self._modifier = MODIFIERS.get(code, None)

    def __str__(self) -> str:
        if self._modifier is None:
            return ""

        return self._modifier.lower()

    @property
    def modifier(self) -> Optional[str]:
        """Get the modifier description of the report."""
        return self._modifier


class ModifierMixin:
    """Mixin to add modifier attribute to the report."""

    def __init__(self) -> None:
        self._modifier = Modifier(None)

    def _handle_modifier(self, match: re.Match) -> None:
        self._modifier = Modifier(match.string)

        self._concatenate_string(self._modifier)

    @property
    def modifier(self) -> Modifier:
        """Get the modifier type of the report."""
        return self._modifier
