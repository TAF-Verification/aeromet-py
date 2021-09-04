import re

from .descriptors import CodeDescriptor
from .weather import Description, Obscuration, Other, Precipitation


class RecentWeather:

    __code = CodeDescriptor()
    __description = Description()
    __precipitation = Precipitation()
    __obscuration = Obscuration()
    __other = Other()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__description = None
            self.__precipitation = None
            self.__obscuration = None
            self.__other = None
        else:
            self.__code = match.string
            self.__description = match.group("descrip")
            self.__precipitation = match.group("precip")
            self.__obscuration = match.group("obsc")
            self.__other = match.group("other")

    def __str__(self):
        s = "{} {} {} {}".format(
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
