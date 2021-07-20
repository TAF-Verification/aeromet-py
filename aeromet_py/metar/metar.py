import re
from typing import List
from collections import namedtuple

import aeromet_py.models as models
from aeromet_py.models import REGEXP


GroupHandler = namedtuple("GroupHandler", "regex func")


class Metar(models.Report):
    """Parser for METAR code."""
    
    __sections = models.MetarSections()
    __type = models.Type()

    def __init__(self, code: str):
        super().__init__(code)
        self.__sections = super().raw_code
        
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
    
    def __parse_body(self):
        handlers = [
            GroupHandler(REGEXP.TYPE, self.__handle_type),
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
        
        if self.unparsed_groups:
            raise models.ParserError(
                "failed while processing {} from METAR: {}".format(
                    self.unparsed_groups,
                    self.raw_code,
                )
            )
    
    def _parse(self):
        self.__parse_body()
