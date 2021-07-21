import re
from typing import List

from aeromet_py.utils import REGEXP

from .data_descriptor import DataDescriptor

trend_re = REGEXP.TREND.replace("^", "").replace("$", "")
rmk_re = REGEXP.REMARK.replace("^", "").replace("$", "")


class MetarSections(DataDescriptor):
    def _handler(self, code: str) -> List[str]:
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
