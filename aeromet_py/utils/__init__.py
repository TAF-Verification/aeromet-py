import re
from typing import Callable

from .conversions import Conversions
from .regexp import RegularExpresions
from .sky_translations import SkyTranslations

REGEXP = RegularExpresions()
SKY_TRANSLATIONS = SkyTranslations()
CONVERSIONS = Conversions()


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


def handle_value(value, conversion):
    if value is None:
        return None

    return value * conversion


def handle_temperature(value: float, conversion: Callable):
    if value is None:
        return None

    return conversion(value)
