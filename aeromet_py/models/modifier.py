import re
from typing import Dict

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

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self._modifier = MODIFIERS.get(code, None)

    def __str__(self) -> str:
        if self._modifier is None:
            return ""

        return self._modifier.lower()

    @property
    def modifier(self) -> str:
        """Get the modifier description of the report."""
        return self._modifier
