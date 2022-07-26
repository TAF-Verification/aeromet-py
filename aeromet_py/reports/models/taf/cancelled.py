import re

from typing import Any, Dict, Optional

from ..base import Group


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

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "is_cancelled": self.is_cancelled,
        }
        d.update(super().as_dict())
        return d
