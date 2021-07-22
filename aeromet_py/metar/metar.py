import re
from collections import namedtuple
from typing import List

import aeromet_py.models as models
from aeromet_py.models import REGEXP

GroupHandler = namedtuple("GroupHandler", "regex func")


class Metar(models.Report):
    """Parser for METAR code."""

    __sections = models.MetarSectionsDescriptor()
    __type = models.Type("METAR")
    __modifier = models.Modifier(None)
    __time = models.Time(None)
    __station = models.Station(None)

    def __init__(self, code: str, year=None, month=None, truncate=False):
        super().__init__(code)
        self.__sections = super().raw_code
        self.__year = year
        self.__month = month
        self.__truncate = truncate

        self._parse()
    
    @property
    def code(self) -> str:
        return super().raw_code

    @property
    def sections(self) -> List[str]:
        return self.__sections

    # Body handlers and its repesctive property

    def __handle_type(self, match: re.Match):
        self.__type = models.Type(match.string)

    @property
    def type(self) -> models.Type:
        return self.__type
    
    def __handle_station(self, match: re.Match):
        self.__station = models.Station(match.string)
    
    @property
    def station(self) -> models.Station:
        return self.__station

    def __handle_time(self, match: re.Match):
        self.__time = models.Time(match.string, year=self.__year, month=self.__month)
    
    @property
    def time(self) -> models.Time:
        return self.__time

    def __handle_modifier(self, match: re.Match):
        self.__modifier = models.Modifier(match.string)

    @property
    def modifier(self) -> models.Modifier:
        return self.__modifier

    def __parse_body(self):
        handlers = [
            GroupHandler(REGEXP.TYPE, self.__handle_type),
            GroupHandler(REGEXP.STATION, self.__handle_station),
            GroupHandler(REGEXP.TIME, self.__handle_time),
            GroupHandler(REGEXP.MODIFIER, self.__handle_modifier),
        ]

        index = 0
        for group in self.__sections[0].split(" "):
            self.unparsed_groups.append(group)

            for handler in handlers[index:]:
                match = re.match(handler.regex, group)
                if match:
                    handler.func(match)
                    index += 1
                    self.unparsed_groups.remove(group)
                    break

        if self.unparsed_groups and self.__truncate:
            raise models.ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )

    def _parse(self):
        self.__parse_body()
