from .descriptors import DataDescriptor, CodeDescriptor
import re
from typing import Tuple

_trend = {
    "NOSIG": "no significant changes",
    "BECMG": "becoming",
    "TEMPO": "temporary",
    "PROB30": "probability 30%",
    "PROB40": "probability 40%",
}
_period = {"FM": "from", "TL": "until", "AT": "at"}


class TrendDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return _trend.get(code, None)


class PeriodPrefixDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return _period.get(code, None)


class PeriodTimeDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        if code[:2] == "24":
            return f"00:{code[2:]}Z"

        return f"{code[:2]}:{code[2:]}Z"


class Period:
    __code = CodeDescriptor()
    __prefix = PeriodPrefixDescriptor()
    __time = PeriodTimeDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__prefix = None
            self.__time = None
        else:
            self.__code = match.string
            self.__prefix = match.group("prefix")
            self.__time = match.group("time")

    def __str__(self):
        if self.__prefix and self.__time:
            return "{} {}".format(self.prefix, self.time)

        return ""

    @property
    def code(self) -> str:
        return self.__code

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def time(self) -> str:
        return self.__time


class Trend:
    __code = CodeDescriptor()
    __trend = TrendDescriptor()

    def __init__(self, match: re.Match):
        self.__from = Period(None)
        self.__until = Period(None)
        self.__at = Period(None)

        if match is None:
            self.__code = None
            self.__trend = None
        else:
            self.__code = match.string
            self.__trend = match.group("trend")

    def __str__(self):
        if self.__trend:
            s = "{} {} {} {}".format(self.trend, self.__from, self.__until, self.__at)
            s = re.sub(r"\s{2,}", " ", s)

            return s.strip()

        return ""

    @property
    def codes(self) -> Tuple[str]:
        return tuple(
            [self.__code]
            + [
                time.code
                for time in [self.__from, self.__until, self.__at]
                if time.code
            ]
        )

    def __period(self, match: re.Match) -> Period:
        if match:
            return Period(match)

        return None

    @property
    def trend(self) -> str:
        return self.__trend

    @property
    def from_time(self) -> str:
        return self.__from.time

    @from_time.setter
    def from_time(self, value: str):
        self.__from = self.__period(value)

    @property
    def until_time(self) -> str:
        return self.__until.time

    @until_time.setter
    def until_time(self, value: str):
        self.__until = self.__period(value)

    @property
    def at_time(self) -> str:
        return self.__at.time

    @at_time.setter
    def at_time(self, value: str):
        self.__at = self.__period(value)
