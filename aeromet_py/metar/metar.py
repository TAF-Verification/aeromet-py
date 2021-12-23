import re
from collections import namedtuple
from typing import List

import aeromet_py.models as models
from aeromet_py.models.mixins import *
from aeromet_py.utils import RegularExpresions, sanitize_visibility, sanitize_windshear

GroupHandler = namedtuple("GroupHandler", "regexp func")


class Metar(models.Report, ModifierMixin, WindMixin, VisibilityMixin):
    """Parser for METAR reports."""

    def __init__(
        self, code: str, year: int = None, month: int = None, truncate: bool = False
    ) -> None:
        super().__init__(code, year=year, month=month)
        ModifierMixin.__init__(self)
        WindMixin.__init__(self)
        VisibilityMixin.__init__(self)
        self._sections = _handle_sections(self._raw_code)
        self._truncate = truncate

        # Body groups
        self._wind_variation = models.WindVariation(None)
        self._minimum_visibility = models.MinimumVisibility(None)

        # Parsers
        self._parse_body()

    @property
    def body(self) -> str:
        """Returns the body section of the METAR report.

        Returns:
            str: the body section.
        """
        return self._sections[0]

    @property
    def trend(self) -> str:
        """Returns the trend section of the METAR report.

        Returns:
            str: the trend section.
        """
        return self._sections[1]

    @property
    def remark(self) -> str:
        """Returns the remark sections of the METAR report.

        Returns:
            str: the remark section.
        """
        return self._sections[2]

    def _handle_time(self, match: re.Match) -> None:
        self._time = models.Time.from_METAR(match.string, self._year, self._month)

        self._concatenate_string(self._time)

    def _handle_wind_variation(self, match: re.Match) -> None:
        self._wind_variation = models.WindVariation(match)

        self._concatenate_string(self._wind_variation)

    @property
    def wind_variation(self) -> models.WindVariation:
        """Returns the wind variation data of the METAR.

        Returns:
            models.WindVariation: the wind variation class instance.
        """
        return self._wind_variation

    def _handle_minimum_visibility(self, match: re.Match) -> None:
        self._minimum_visibility = models.MinimumVisibility(match)

        self._concatenate_string(self._minimum_visibility)

    @property
    def minimum_visibility(self) -> models.MinimumVisibility:
        """Returns the minimum visibility data of the METAR.

        Returns:
            models.Visibility: the minimum visibility class instance.
        """
        return self._minimum_visibility

    def _parse_body(self) -> None:
        handlers = [
            GroupHandler(RegularExpresions.TYPE, self._handle_type),
            GroupHandler(RegularExpresions.STATION, self._handle_station),
            GroupHandler(RegularExpresions.TIME, self._handle_time),
            GroupHandler(RegularExpresions.MODIFIER, self._handle_modifier),
            GroupHandler(RegularExpresions.WIND, self._handle_wind),
            GroupHandler(RegularExpresions.WIND_VARIATION, self._handle_wind_variation),
            GroupHandler(RegularExpresions.VISIBILITY, self._handle_visibility),
            GroupHandler(RegularExpresions.VISIBILITY, self._handle_minimum_visibility),
        ]

        self._parse(handlers, self.body)

    def _parse(
        self, handlers: List[GroupHandler], section: str, section_type: str = "body"
    ) -> None:
        """Parse the groups of section_type.

        Args:
            handlers (List[GroupHandler]): handler list to manage and match.
            section (str): the section containing all the groups to parse.
            section_type (str, optional): the section type to parse. Defaults to "body".

        Raises:
            models.ParserError: if self.unparser_groups has items and self.__truncate == True,
            raises the error.
        """
        index = 0
        section = sanitize_visibility(section)
        if section_type == "body":
            section = sanitize_windshear(section)

        for group in section.split(" "):
            self.unparsed_groups.append(group)

            for handler in handlers[index:]:
                match = re.match(handler.regexp, group)
                index += 1
                if match:
                    handler.func(match)
                    self.unparsed_groups.remove(group)
                    break

        if self.unparsed_groups and self._truncate:
            raise models.ParserError(
                "failed while processing {} from: {}".format(
                    ", ".join(self.unparsed_groups),
                    self.raw_code,
                )
            )


def _handle_sections(code: str) -> List[str]:
    trend_re = RegularExpresions.TREND.replace("^", "").replace("$", "")
    rmk_re = RegularExpresions.REMARK.replace("^", "").replace("$", "")

    try:
        trend_pos = re.search(trend_re, code).start()
    except AttributeError:
        trend_pos = None
    try:
        rmk_pos = re.search(rmk_re, code).start()
    except AttributeError:
        rmk_pos = None

    if trend_pos is None and rmk_pos is not None:
        body = code[: rmk_pos - 1]
        rmk = code[rmk_pos:]
        trend = ""
    elif trend_pos is not None and rmk_pos is None:
        body = code[: trend_pos - 1]
        trend = code[trend_pos:]
        rmk = ""
    elif trend_pos is None and rmk_pos is None:
        body = code
        trend = ""
        rmk = ""
    else:
        if trend_pos > rmk_pos:
            body = code[: rmk_pos - 1]
            rmk = code[rmk_pos : trend_pos - 1]
            trend = code[trend_pos:]
        else:
            body = code[: trend_pos - 1]
            trend = code[trend_pos : rmk_pos - 1]
            rmk = code[rmk_pos:]

    return [body, trend, rmk]
