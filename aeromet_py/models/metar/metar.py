import re

from aeromet_py.utils import MetarRegExp

from ..report import Report


class Metar(Report):
    """Parser for METAR reports."""

    def __init__(self, code: str) -> None:
        super().__init__(code)

        self._handle_sections()

    def _handle_sections(self) -> None:
        trend_re: re.Pattern = re.compile(
            MetarRegExp.TREND.replace("^", "").replace("$", "")
        )
        remark_re: re.Pattern = re.compile(
            MetarRegExp.REMARK.replace("^", "").replace("$", "")
        )

        trend_pos: int = None
        remark_pos: int = None

        try:
            trend_pos = trend_re.search(self._raw_code).start()
        except AttributeError:
            pass

        try:
            remark_pos = remark_re.search(self._raw_code).start()
        except AttributeError:
            pass

        body: str = ""
        trend: str = ""
        remark: str = ""

        if trend_pos is None and remark_pos is not None:
            body = self._raw_code[: remark_pos - 1]
            remark = self._raw_code[remark_pos:]
        elif trend_pos is not None and remark_pos is None:
            body = self._raw_code[: trend_pos - 1]
            trend = self._raw_code[trend_pos:]
        elif trend_pos is None and remark_pos is None:
            body = self._raw_code
        else:
            if trend_pos > remark_pos:
                body = self._raw_code[: remark_pos - 1]
                remark = self._raw_code[remark_pos : trend_pos - 1]
                trend = self._raw_code[trend_pos:]
            else:
                body = self._raw_code[: trend_pos - 1]
                trend = self._raw_code[trend_pos : remark_pos - 1]
                remark = self._raw_code[remark_pos:]

        self._sections = [body, trend, remark]

    def _parse(self) -> None:
        return super()._parse()

    @property
    def body(self) -> str:
        """Get the body part of the METAR."""
        return self._sections[0]

    @property
    def trend(self) -> str:
        """Get the trend part of the METAR."""
        return self._sections[1]

    @property
    def remark(self) -> str:
        """Get the remark part of the METAR."""
        return self._sections[2]
