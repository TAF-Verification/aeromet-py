import re
from typing import Iterator, List, Tuple

from aeromet_py.utils import SKY_TRANSLATIONS

from .descriptors import CodeDescriptor, DataDescriptor


class Intensity(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.WEATHER_INT.get(code, None)


class Description(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.WEATHER_DESC.get(code, None)


class Precipitation(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.WEATHER_PREC.get(code, None)


class Obscuration(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.WEATHER_OBSC.get(code, None)


class Other(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.WEATHER_OTHER.get(code, None)


class Weather:

    __code = CodeDescriptor()
    __intensity = Intensity()
    __description = Description()
    __precipitation = Precipitation()
    __obscuration = Obscuration()
    __other = Other()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__intensity = None
            self.__description = None
            self.__precipitation = None
            self.__obscuration = None
            self.__other = None
        else:
            self.__code = match.string
            self.__intensity = match.group("int")
            self.__description = match.group("desc")
            self.__precipitation = match.group("prec")
            self.__obscuration = match.group("obsc")
            self.__other = match.group("other")

    def __str__(self):
        s = "{} {} {} {} {}".format(
            self.__intensity,
            self.__description,
            self.__precipitation,
            self.__obscuration,
            self.__other,
        )
        s = s.replace("None", "")
        s = re.sub(r"\s{2,}", " ", s)

        return s.strip()

    @property
    def code(self) -> str:
        return self.__code

    @property
    def intensity(self) -> str:
        return self.__intensity

    @property
    def description(self) -> str:
        return self.__description

    @property
    def precipitation(self) -> str:
        return self.__precipitation

    @property
    def obscuration(self) -> str:
        return self.__obscuration

    @property
    def other(self) -> str:
        return self.__other


class WeathersDescriptor(DataDescriptor):
    def _handler(self, match: re.Match):
        return Weather(match)


class Weathers:

    __first = WeathersDescriptor()
    __second = WeathersDescriptor()
    __third = WeathersDescriptor()

    def __init__(self):
        self.__count = 0
        self.__first = None
        self.__second = None
        self.__third = None
        self.__list = []

    def add(self, match: re.Match):
        if self.__count == 3:
            raise AttributeError("can't set more than three weather codes")

        if self.__count == 0:
            self.__first = match
            self.__list.append(self.__first)
        elif self.__count == 1:
            self.__second = match
            self.__list.append(self.__second)
        else:
            self.__third = match
            self.__list.append(self.__third)

        self.__count += 1

    def __list_of_str(self):
        return [str(weather) for weather in self.__list]

    def __str__(self):
        return " | ".join(self.__list_of_str())

    def __len__(self):
        return len(self.__list)

    def __iter__(self) -> Iterator[Weather]:
        return iter(self.__list)

    @property
    def to_list(self) -> List[str]:
        return self.__list_of_str()

    @property
    def codes(self) -> Tuple[str]:
        return tuple(weather.code for weather in self.__list)

    @property
    def first(self) -> Weather:
        return self.__first

    @property
    def second(self) -> Weather:
        return self.__second

    @property
    def third(self) -> Weather:
        return self.__third
