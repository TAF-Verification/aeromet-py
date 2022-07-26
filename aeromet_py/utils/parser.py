import re

from typing import List


def sanitize_visibility(report: str) -> str:
    """Sanitize the visibility in sea miles to get macth
    with the regular expresion of visibility in METAR like
    reports.

    Args:
        report (str): the report or section to sanitize.

    Returns:
        str: the sanitized report or section.
    """
    regex = r"\s(?P<int>\d+)\s(?P<frac>\d/\dSM)\s?"

    for _ in range(3):
        match = re.search(regex, report)

        try:
            report = re.sub(regex, " {}_{} ".format(*match.groups()), report, count=1)
        except AttributeError:
            break

    return report


def sanitize_windshear(report: str) -> str:
    """Sanitize the windshear in to get macth with the
    regular expresion of windshear in METAR like reports.

    Args:
        report (str): the report or section to sanitize.

    Returns:
        str: the sanitized report or section.
    """
    report = re.sub(r"WS\sALL\sRWY", "WS_ALL_RWY", report)

    fmt = r"WS\sR(WY)?(?P<name>\d{2}[CLR]?)"
    pattern = re.compile(fmt)
    for _ in range(3):
        match = pattern.search(report)
        if match:
            report = re.sub(fmt, "WS_R{}".format(match.group("name")), report, count=1)

    return report


def sanitize_change_indicator(report: str) -> str:
    """Sanitize the `PROB[34]0 TEMPO` to get match with the
    regular expression of the change indicator in TAF like reports.

    Args:
        report (str): the report or section to sanitize.

    Returns:
        str: the sanitized report or section.
    """
    fmt = r"PROB(?P<percent>[34]0)\sTEMPO"
    pattern = re.compile(fmt)
    for _ in range(5):
        match = pattern.search(report)
        if match:
            report = re.sub(
                fmt, "PROB{}_TEMPO".format(match.group("percent")), report, count=1
            )
        else:
            break

    return report
