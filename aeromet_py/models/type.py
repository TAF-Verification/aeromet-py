from .data_descriptor import DataDescriptor

_description = {
    "METAR": "Meteorological Aerodrome Report",
    "SPECI": "Special Aerodrome Report",
    "TAF": "Terminal Aerodrome Forecast",
}


class Type(DataDescriptor):

    def _handler(self, value):
        return _description.get(value, None)
