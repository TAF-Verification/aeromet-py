import re

from ..visibility import Prevailing


class VisibilityMixin:
    """Mixin to add visibility attribute to the report."""

    def __init__(self) -> None:
        self._visibility = Prevailing(None)

    def _handle_visibility(self, match: re.Match) -> None:
        self._visibility = Prevailing(match)

        self._concatenate_string(self._visibility)

    @property
    def visibility(self) -> Prevailing:
        """Returns the prevailing visibility data of the report.

        Returns:
            models.Prevailing: the prevailing visibility class instance.
        """
        return self._visibility
