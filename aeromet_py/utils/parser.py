import re
from typing import List

from ..models.group import GroupHandler


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


def parse_section(handlers: List[GroupHandler], section: str) -> List[str]:
    """Parse the groups of the section.

    Args:
        handlers (List[GroupHandler]): handler list to manage and match.
        section (str): the section containing all the groups to parse separated
        by spaces.

    Returns:
        unparsed_groups (List[str]): the not matched groups with anyone
            of the regular expresions stored in `handlers`.
    """
    unparsed_groups: List[str] = []
    index: int = 0

    for group in section.split(" "):
        unparsed_groups.append(group)
        for group_handler in handlers[index:]:
            match = re.match(group_handler.regexp, group)
            index += 1
            if match:
                group_handler.handler(match)
                unparsed_groups.remove(group)
                break

    return unparsed_groups
