from typing import Any, Dict, Optional

from ..base import Modifier


class Missing(Modifier):
    """Basic structure for missing TAF."""

    def __init__(self, code: Optional[str]) -> None:
        super().__init__(code)

        if code != None:
            self._missing = True
        else:
            self._missing = False

    @property
    def is_missing(self) -> bool:
        """Get if the TAF is missing."""
        return self._missing

    def as_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "is_missing": self.is_missing,
        }
        d.update(super().as_dict())
        return d
