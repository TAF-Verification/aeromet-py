import re

from aeromet_py.models.modifier import Modifier


class ModifierMixin:
    """Mixin to add modifier attribute to the report."""

    def __init__(self) -> None:
        self._modifier = Modifier(None)

    def _handle_modifier(self, match: re.Match) -> None:
        self._modifier = Modifier(match.string)

        self._concatenate_string(self._modifier)

    @property
    def modifier(self) -> Modifier:
        """Get the modifier type of the report."""
        return self._modifier
