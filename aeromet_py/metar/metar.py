import re
from typing import List

import aeromet_py.models as models
from aeromet_py.utils import REGEXP


class Metar(models.Report):
    """Parser for METAR reports."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self._sections = _handle_sections(self._raw_code)

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

    def _parse(self) -> None:
        return super()._parse()


def _handle_sections(code: str) -> List[str]:
    trend_re = REGEXP.TREND.replace("^", "").replace("$", "")
    rmk_re = REGEXP.REMARK.replace("^", "").replace("$", "")

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
