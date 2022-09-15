from typing import Dict, Optional

from .group import Group


TYPES: Dict[str, str] = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class ReportType(Group):
    """Basic structure for type groups in reports from land stations."""

    def __init__(self, code: str):
        super().__init__(code)
        self._type = TYPES.get(code, None)

    def __str__(self) -> str:
        return f"{self._type} ({self._code})"

    @property
    def type_(self) -> str:
        """Get the type of the report."""
        return self._type

    def as_dict(self) -> Dict[str, Optional[str]]:
        d = {
            "type": self.type_,
        }
        d.update(super().as_dict())
        return d
