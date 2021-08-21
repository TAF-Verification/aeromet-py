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

    print(report)
    for _ in range(3):
        match = re.search(regex, report)

        try:
            report = re.sub(regex, " {}_{} ".format(*match.groups()), report, count=1)
        except AttributeError:
            break

    return report


def handle_distance(value, conversion):
    if value is None:
        return None

    return value * conversion


def handle_temperature(value: float, conversion: Callable):
    if value is None:
        return None

    return conversion(value)
