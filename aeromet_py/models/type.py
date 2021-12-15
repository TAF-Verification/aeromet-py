from .descriptor import DataDescriptor

_description = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class Type:

    _code = DataDescriptor()
    _type = DataDescriptor()

    def __init__(self, code: str):
        self._code = code
        self._type = _description.get(code, None)

    def __str__(self) -> str:
        return f"{self.type} ({self.code})"

    @property
    def code(self) -> str:
        """Returns the code of the type group.

        Returns:
            str: the type code.
        """
        return self._code

    @property
    def type(self) -> str:
        """Returns the type of the report.

        Returns:
            str: the type of the report.
        """
        return self._type
