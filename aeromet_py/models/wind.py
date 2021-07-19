from typing import Any

from .metaf_base import DataDescriptor


class Direction(DataDescriptor):
    def __init__(self, name: str):
        super().__init__(name)

    def _handler(self, value):
        return float(value)


class Speed(DataDescriptor):
    def __init__(self, name: str):
        super().__init__(name)

    def _handler(self, value):
        return float(value)


class Wind:

    __direction = Direction("direction")
    __speed = Speed("speed")
    __gust = Speed("gust")

    def __init__(self, group: str):
        self.__group = group
        self.__direction = group[:3]
        self.__speed = group[3:5]
        self.__gust = group[6:8]

    @property
    def direction_in_degrees(self):
        return self.__direction

    @property
    def direction_in_radians(self):
        return self.__direction * 3.14 / 180

    @property
    def speed_in_mps(self):
        return self.__speed

    @property
    def speed_in_kph(self):
        return self.__speed * 3.6

    @property
    def gust(self):
        return self.__gust
