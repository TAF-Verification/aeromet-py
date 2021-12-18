from typing import Dict

from .descriptor import DataDescriptor
from .group import Group

_description: Dict[str, str] = {
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

    _modifier = DataDescriptor()

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self._modifier = _description.get(code, None)

    def __str__(self) -> str:
        if self._modifier is not None:
            return self._modifier.lower()
        return ""

    @property
    def modifier(self) -> str:
        """Returns the modifier description of the report.

        Returns:
            str: the description.
        """
        return self._modifier
