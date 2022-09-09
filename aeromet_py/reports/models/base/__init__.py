import re

from typing import List

from .change_indicator import ChangeIndicator
from .cloud import Cloud, CloudList
from .distance import Distance
from .errors import ParserError, RangeError
from .flight_rules import FlightRulesMixin
from .group import Group, GroupHandler, GroupList
from .modifier import Modifier, ModifierMixin
from .numeric import Numeric
from .pressure import Pressure
from .report import Report
from .station import Station
from .string_attribute import HasConcatenateStringProntocol, StringAttributeMixin
from .temperature import Temperature
from .time import Time, TimeMixin
from .type import ReportType
from .wind import Direction, Speed, Wind


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
        counter = 0

        for group_handler in handlers[index:]:
            match = re.match(group_handler.regexp, group)
            counter += 1

            if match:
                index += counter
                group_handler.handler(match)
                unparsed_groups.remove(group)
                break

    return unparsed_groups
