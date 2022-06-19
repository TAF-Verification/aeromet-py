from typing import Any

from typing_extensions import Protocol


class HasConcatenateStringProntocol(Protocol):
    def _concatenate_string(self, obj: Any) -> None:
        pass


class StringAttributeMixin:
    """Basic structure to add string helpers to the report."""

    def __init__(self) -> None:
        # String buffer
        self._string = ""

    def __str__(self) -> str:
        return self._string.strip()

    def _concatenate_string(self, obj: Any) -> None:
        self._string += str(obj) + "\n"
