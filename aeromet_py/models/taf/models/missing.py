import re

from ...modifier import Modifier


class Missing(Modifier):
    """Basic structure for missing TAF."""

    def __init__(self, code: str) -> None:
        super().__init__(code)

        if code != None:
            self._missing = True
        else:
            self._missing = False

    @property
    def is_missing(self) -> bool:
        """Get if the TAF is missing."""
        return self._missing
