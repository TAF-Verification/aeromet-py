import re

from typing import List

from ....utils import (
    MetarRegExp,
    TafRegExp,
    sanitize_change_indicator,
    sanitize_visibility,
)
from ..base import GroupHandler, GroupList, parse_section
from ..metar import Forecast
from .change_indicator import TafChangeIndicator
from .valid import Valid


class ChangeForecasted(Forecast):
    """Basic structure for significant change periods in TAF."""

    def __init__(self, code: str, valid: Valid) -> None:
        super().__init__(code)

        # Initialize valid period of the forecasts
        self._valid = valid

        # Groups
        self._change_indicator = TafChangeIndicator(None, valid)

        # Parse groups
        self._parse()

    def __str__(self) -> str:
        self._string = ""
        self._concatenate_string(self._change_indicator)

        return self._string

    def _handle_change_indicator(self, match: re.Match) -> None:
        self._change_indicator = TafChangeIndicator(match, self._valid)

    @property
    def change_indicator(self) -> TafChangeIndicator:
        """Get the change indicator data of the change period."""
        return self._change_indicator

    def _handle_valid_period(self, match: re.Match) -> None:
        self._change_indicator.set_valid_period(match, self._valid.period_from)

    def _parse(self) -> None:
        handlers: List[GroupHandler] = [
            GroupHandler(TafRegExp.CHANGE_INDICATOR, self._handle_change_indicator),
            GroupHandler(TafRegExp.VALID, self._handle_valid_period),
            GroupHandler(TafRegExp.WIND, self._handle_wind),
            GroupHandler(MetarRegExp.VISIBILITY, self._handle_prevailing),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.WEATHER, self._handle_weather),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
            GroupHandler(MetarRegExp.CLOUD, self._handle_cloud),
        ]

        sanitized_code = sanitize_change_indicator(self._code)
        sanitized_code = sanitize_visibility(sanitized_code)
        unparsed: List[str] = parse_section(handlers, sanitized_code)
        self._unparsed_groups += unparsed


class TafChangesForecasted(GroupList[ChangeForecasted]):
    """Basic structure for weather change periods in TAF."""

    def __init__(self) -> None:
        super().__init__(8)

    def __str__(self) -> str:
        return "\n".join(str(change) for change in self._list)

    def add(self, new_change: ChangeForecasted) -> None:
        """Adds weather changes to the list."""
        if len(self._list) > 0:
            if new_change.code.startswith("FM") or new_change.code.startswith("BECMG"):
                temp_changes: List[ChangeForecasted] = []

                last_change: ChangeForecasted = self._list.pop()
                while True:
                    if last_change.change_indicator.code.startswith(
                        "PROB"
                    ) or last_change.change_indicator.code.startswith("TEMPO"):
                        temp_changes.append(last_change)
                        try:
                            last_change = self._list.pop()
                        except IndexError:
                            break
                    elif last_change.change_indicator.code.startswith("FM"):
                        last_change.change_indicator.reset_until_period(
                            new_change.change_indicator.valid.period_from
                        )
                        temp_changes.append(last_change)
                        break
                    else:
                        temp_changes.append(last_change)
                        break

                temp_changes.reverse()
                for temp_change in temp_changes:
                    super().add(temp_change)

        super().add(new_change)
