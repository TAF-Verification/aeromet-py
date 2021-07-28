import re

from .regexp import RegularExpresions

REGEXP = RegularExpresions()


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
