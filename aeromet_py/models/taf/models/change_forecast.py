import re
from typing import List

from ...metar.models import Forecast
from ...group import GroupHandler, GroupList
from ....utils import TafRegExp, parse_section, sanitize_change_indicator
from .change_indicator import TafChangeIndicator
from .valid import Valid


class ChangeForecast(Forecast):
    """Basic structure for significant change periods in TAF."""

    def __init__(self, code: str, valid: Valid) -> None:
        super().__init__(code)

        # Initialize valid period of the forecasts
        self._valid = valid

        # Groups
        self._change_indicator = TafChangeIndicator(None, valid)

        # Parse groups
        self._parse()

    def _handle_change_indicator(self, match: re.Match) -> None:
        self._change_indicator = TafChangeIndicator(match, self._valid)

    @property
    def change_indicator(self) -> TafChangeIndicator:
        """Get the change indicator data of the change period."""
        return self._change_indicator

    def _parse(self) -> None:
        handlers: List[GroupHandler] = [
            GroupHandler(TafRegExp.CHANGE_INDICATOR, self._handle_change_indicator),
        ]

        sanitized_code = sanitize_change_indicator(self._code)
        unparsed: List[str] = parse_section(handlers, sanitized_code)
        self._unparsed_groups += unparsed


class TafChangePeriods(GroupList[ChangeForecast]):
    """Basic structure for weather change periods in TAF."""

    def __init__(self) -> None:
        super().__init__(8)

    def __str__(self) -> str:
        return "\n".join(str(change) for change in self._list)
