import re

from ...metar.models import MetarPrevailingVisibility


class MetarPrevailingMixin:
    """Mixin to add prevailing visibility attribute to the report."""

    def __init__(self) -> None:
        self._prevailing = MetarPrevailingVisibility(None)

    def _handle_prevailing(self, match: re.Match) -> None:
        print("from _handle_prevailing")
        self._prevailing = MetarPrevailingVisibility(match)

        self._concatenate_string(self._prevailing)

    @property
    def prevailing_visibility(self) -> MetarPrevailingVisibility:
        """Get the prevailing visibility data of the report."""
        return self._prevailing
