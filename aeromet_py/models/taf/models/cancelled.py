import re
from typing import Optional

from ...group import Group


class Cancelled(Group):
    """Basic structure for cancelled groups in TAF."""

    def __init__(self, match: Optional[re.Match]) -> None:
        self._is_cancelled = False

        if match is None:
            super().__init__(None)
        else:
            super().__init__(match.string)
            self._is_cancelled = True

    def __str__(self) -> str:
        if self._is_cancelled:
            return "cancelled"

        return ""

    @property
    def is_cancelled(self) -> bool:
        """Get if the TAF is cancelled."""
        return self._is_cancelled
