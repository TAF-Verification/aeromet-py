import re

from ..wind import Wind


class WindMixin:
    """Mixin to add wind attribute to the report."""

    def __init__(self) -> None:
        self._wind = Wind(None)

    def _handle_wind(self, match: re.Match) -> None:
        self._wind = Wind(match)

        self._concatenate_string(self._wind)

    @property
    def wind(self) -> Wind:
        """Returns the wind data of the report.

        Returns:
            Wind: the wind class instance.
        """
        return self._wind
