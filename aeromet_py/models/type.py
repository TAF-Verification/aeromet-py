from .descriptors import CodeDescriptor, DataDescriptor

_description = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class TypeDescriptor(DataDescriptor):
    def _handler(self, value):
        return _description.get(value, None)


class Type:

    __code = CodeDescriptor()
    __type = TypeDescriptor()

    def __init__(self, code: str):
        self.__code = code
        self.__type = self.__code

    @property
    def code(self) -> str:
        return self.__code

    @property
    def type(self) -> str:
        return self.__type

    def __str__(self) -> str:
        return f"{self.__code}: {self.__type}"
