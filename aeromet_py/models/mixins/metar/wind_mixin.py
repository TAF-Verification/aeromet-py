import re

from ...metar.models.wind import MetarWind


class MetarWindMixin:
    """Mixin to add a METAR wind group attribute to the report."""

    def __init__(self) -> None:
        self._wind = MetarWind(None)

    def _handle_wind(self, match: re.Match) -> None:
        self._wind = MetarWind(match)

        self._concatenate_string(self._wind)

    @property
    def wind(self) -> MetarWind:
        """Get the wind data of the report."""
        return self._wind
