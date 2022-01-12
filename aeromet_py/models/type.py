from typing import Dict

from .group import Group

TYPES: Dict[str, str] = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class Type(Group):
    """Basic structure for type groups in reports from land stations."""

    def __init__(self, code: str):
        super().__init__(code)
        self._type = TYPES.get(code, None)

    def __str__(self) -> str:
        return f"{self._type} ({self._code})"

    @property
    def type(self) -> str:
        """Get the type of the report."""
        return self._type
