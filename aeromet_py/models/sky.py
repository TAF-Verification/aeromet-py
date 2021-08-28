import re
from typing import Iterator, List, Tuple

from aeromet_py.utils import CONVERSIONS, SKY_TRANSLATIONS, handle_value

from .descriptors import CodeDescriptor, DataDescriptor


class CoverDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.SKY_COVER.get(code, None)


class HeightDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        if code == "///":
            return None

        return float(code) * 100


class CloudDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SKY_TRANSLATIONS.CLOUD_TYPE.get(code, None)


class CloudLayer:

    __code = CodeDescriptor()
    __cover = CoverDescriptor()
    __height = HeightDescriptor()
    __cloud = CloudDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__cover = None
            self.__height = None
            self.__cloud = None
        else:
            self.__code = match.string
            self.__cover = match.group("cover")
            self.__height = match.group("height")
            self.__cloud = match.group("cloud")

    def __str__(self):
        if self.__cloud and self.__height:
            return "{} at {} feet of {}".format(
                self.__cover,
                self.__height,
                self.__cloud,
            )
        elif self.__height:
            return "{} at {} feet".format(
                self.__cover,
                self.__height,
            )
        elif self._cover == "clear":
            return self._cover
        else:
            return "{} at undefined height", format(
                self.__cover,
            )

    @property
    def code(self) -> str:
        return self.__code

    @property
    def cover(self) -> str:
        return self.__cover

    @property
    def height_in_meters(self) -> float:
        return handle_value(self.__height, CONVERSIONS.FT_TO_M)

    @property
    def height_in_kilometers(self) -> float:
        return handle_value(self.__height, CONVERSIONS.FT_TO_M * CONVERSIONS.M_TO_KM)

    @property
    def height_in_sea_miles(self) -> float:
        return handle_value(
            self.__height, CONVERSIONS.FT_TO_M * CONVERSIONS.M_TO_SMI
        )

    @property
    def height_in_feet(self) -> float:
        return handle_value(self.__height, 1)

    @property
    def cloud(self) -> str:
        return self.__cloud


class SkyDescriptor(DataDescriptor):
    def _handler(self, match: re.Match):
        return CloudLayer(match)


class Sky:

    __first = SkyDescriptor()
    __second = SkyDescriptor()
    __third = SkyDescriptor()
    __fourth = SkyDescriptor()

    def __init__(self):
        self.__count = 0
        self.__first = None
        self.__second = None
        self.__third = None
        self.__fourth = None
        self.__list = []

    def add(self, match: re.Match):
        if self.__count == 4:
            raise AttributeError("can't set more than four sky codes")

        if self.__count == 0:
            self.__first = match
            self.__list.append(self.__first)
        elif self.__count == 1:
            self.__second = match
            self.__list.append(self.__second)
        elif self.__count == 2:
            self.__third = match
            self.__list.append(self.__third)
        else:
            self.__fourth = match
            self.__list.append(self.__fourth)

        self.__count += 1

    def __list_of_str(self):
        return [str(cloud_layer) for cloud_layer in self.__list]

    def __str__(self):
        return " | ".join(self.__list_of_str())

    def __len__(self):
        return len(self.__list)

    def __iter__(self) -> Iterator[CloudLayer]:
        return iter(self.__list)

    @property
    def to_list(self) -> List[str]:
        return self.__list_of_str()

    @property
    def codes(self) -> Tuple[str]:
        return tuple(layer.code for layer in self.__list)

    @property
    def first(self) -> CloudLayer:
        return self.__first

    @property
    def second(self) -> CloudLayer:
        return self.__second

    @property
    def third(self) -> CloudLayer:
        return self.__third

    @property
    def fourth(self) -> CloudLayer:
        return self.__fourth
