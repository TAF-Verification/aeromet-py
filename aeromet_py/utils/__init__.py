import re

from .regexp import RegularExpresions
from .conversions import Conversions


def sanitize_visibility(report: str) -> str:
    regex = r"\s(?P<int>\d+)\s(?P<frac>\d/\dSM)\s?"

    for _ in range(3):
        match = re.search(regex, report)

        try:
            report = re.sub(regex, " {}_{} ".format(*match.groups()), report, count=1)
        except AttributeError:
            break

    return report


def sanitize_windshear(report: str) -> str:
    report = re.sub(r"WS\sALL\sRWY", "WS_ALL_RWY", report)

    fmt = r"WS\sR(WY)?(?P<name>\d{2}[CLR]?)"
    pattern = re.compile(fmt)
    for _ in range(3):
        match = pattern.search(report)
        if match:
            report = re.sub(fmt, "WS_R{}".format(match.group("name")), report, count=1)

    return report
