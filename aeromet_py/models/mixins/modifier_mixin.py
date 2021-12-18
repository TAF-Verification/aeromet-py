import re

from ..modifier import Modifier


class ModifierMixin:
    def __init__(self) -> None:
        self._modifier = Modifier(None)

    def _handle_modifier(self, match: re.Match) -> None:
        self._modifier = Modifier(match.string)

        self._concatenate_string(self._modifier)

    @property
    def modifier(self) -> Modifier:
        """Returns the modifier data of the report.

        Returns:
            Modifier: the modifier class instance.
        """
        return self._modifier
