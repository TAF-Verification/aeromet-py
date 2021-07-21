from .data_descriptor import DataDescriptor

_description = {
    "COR": "Correction",
    "CORR": "Correction",
    "AMD": "Amendment",
    "NIL": "Missing report",
    "AUTO": "Automatic report",
    "TEST": "Testing report",
    "FINO": "Missing report",
}


class Modifier(DataDescriptor):
    def _handler(self, value):
        return _description.get(value, None)
