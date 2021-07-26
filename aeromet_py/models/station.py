from aeromet_py.database import get_country, get_stations

from .descriptors import CodeDescriptor, DataDescriptor


class StationDescriptor(DataDescriptor):
    def _handler(self, code):
        return code


class Station:

    __code = CodeDescriptor()
    __station = StationDescriptor()

    def __init__(self, code: str):
        self.__code = code
        self.__station = [None for i in range(8)]
        for stn in get_stations():
            if stn[1] == self.__code:
                self.__station = stn
                break

    @property
    def name(self):
        return self.__station[0]

    @property
    def icao(self):
        return self.__station[1]

    @property
    def iata(self):
        return self.__station[2]

    @property
    def synop(self):
        return self.__station[3]

    @property
    def latitude(self):
        return self.__station[4]

    @property
    def longitude(self):
        return self.__station[5]

    @property
    def elevation(self):
        return self.__station[6]

    @property
    def country(self):
        return get_country(self.__station[7])
