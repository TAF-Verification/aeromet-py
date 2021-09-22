from .descriptors import CodeDescriptor, DataDescriptor

_description = {
    "COR": "Correction",
    "CORR": "Correction",
    "AMD": "Amendment",
    "NIL": "Missing report",
    "AUTO": "Automatic report",
    "TEST": "Testing report",
    "FINO": "Missing report",
}


class ModifierDescriptor(DataDescriptor):
    def _handler(self, value):
        return _description.get(value, None)


class Modifier:

    __code = CodeDescriptor()
    __modifier = ModifierDescriptor()

    def __init__(self, code: str):
        self.__code = code
        self.__modifier = self.__code

    def __str__(self):
        if self.__modifier is not None:
            return self.__modifier.lower()

        return ""

    @property
    def code(self) -> str:
        return self.__code

    @property
    def modifier(self) -> str:
        return self.__modifier
