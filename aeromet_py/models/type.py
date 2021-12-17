from .descriptor import DataDescriptor
from .group import Group

_description = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class Type(Group):

    _type = DataDescriptor()

    def __init__(self, code: str):
        super().__init__(code)
        self._type = _description.get(code, None)

    def __str__(self) -> str:
        return f"{self.type} ({self.code})"

    @property
    def type(self) -> str:
        """Returns the type of the report.

        Returns:
            str: the type of the report.
        """
        return self._type
