import re
from collections import namedtuple
from typing import List

import aeromet_py.models as models
from aeromet_py.models import REGEXP

GroupHandler = namedtuple("GroupHandler", "regex func")


class Metar(models.Report):
    """Parser for METAR code."""

    __sections = models.MetarSections()
    __type = models.Type()
    __modifier = models.Modifier()

    def __init__(self, code: str, truncate=False):
        super().__init__(code)
        self.__sections = super().raw_code
        self.__truncate = truncate

        self._parse()

    @property
    def sections(self):
        return self.__sections

    # Body handlers and its repesctive property

    def __handle_type(self, match: re.Match):
        self.__type = match.group("type")

    @property
    def type(self):
        return self.__type

    def __handle_modifier(self, match: re.Match):
        self.__modifier = match.group("mod")

    @property
    def modifier(self):
        return self.__modifier

    def __parse_body(self):
        handlers = [
            GroupHandler(REGEXP.TYPE, self.__handle_type),
            GroupHandler(REGEXP.MODIFIER, self.__handle_modifier),
        ]

        index = 0
        for group in self.__sections[0].split(" "):
            self.unparsed_groups.append(group)

            for i, handler in enumerate(handlers[index:]):
                match = re.match(handler.regex, group)
                if match:
                    handler.func(match)
                    index = i + 1
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
