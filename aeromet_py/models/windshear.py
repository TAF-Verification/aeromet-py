import re
from typing import Iterator, List, Tuple

from .descriptors import CodeDescriptor, DataDescriptor
from .visibility import NameDescriptor


class Runway:

    __code = CodeDescriptor()
    __name = NameDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__name = None
        else:
            self.__code = match.string.replace("_", " ")
            self.__name = match.group("name")

    def __str__(self):
        return self.__name

    @property
    def code(self) -> str:
        return self.__code

    @property
    def runway_name(self) -> str:
        return self.__name


class WindshearDescriptor(DataDescriptor):
    def _handler(self, match: re.Match):
        return Runway(match)


class Windshear:

    __first = WindshearDescriptor()
    __second = WindshearDescriptor()
    __third = WindshearDescriptor()

    def __init__(self):
        self.__all = False
        self.__count = 0
        self.__first = None
        self.__second = None
        self.__third = None
        self.__list = []

    def add(self, match: re.Match):
        if self.__count == 3:
            raise AttributeError("can't set more than three windshear codes")

        if self.__count == 0:
            self.__first = match
            self.__list.append(self.__first)
            if match.group("all"):
                self.__all = True
        elif self.__count == 1:
            self.__second = match
            self.__list.append(self.__second)
        else:
            self.__third = match
            self.__list.append(self.__third)

        self.__count += 1

    def __list_of_str(self):
        return [str(windshear) for windshear in self.__list]

    def __str__(self):
        return " | ".join(self.__list_of_str())

    def __len__(self):
        return len(self.__list)

    def __iter__(self) -> Iterator[Runway]:
        return iter(self.__list)

    @property
    def to_list(self) -> List[str]:
        return self.__list_of_str()

    @property
    def codes(self) -> Tuple[str]:
        return tuple(windshear.code for windshear in self.__list)

    @property
    def first(self) -> Runway:
        return self.__first

    @property
    def second(self) -> Runway:
        return self.__second

    @property
    def thrid(self) -> Runway:
        return self.__third

    @property
    def all_runways(self) -> bool:
        return self.__all
