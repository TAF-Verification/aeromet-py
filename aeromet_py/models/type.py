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
        return self._code

    @property
    def type(self) -> str:
        return self._type
