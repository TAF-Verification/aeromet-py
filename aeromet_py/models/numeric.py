from abc import ABCMeta
from ast import Call
from dataclasses import make_dataclass
from typing import Callable, Union


class Numeric(metaclass=ABCMeta):
    """Basic structure to handle numeric values."""

    def __init__(self, value: float) -> None:
        self._value = value

    def __str__(self) -> str:
        if self._value is None:
            return ""

        return f"{self._value:.1f}"

    def converted(self, conversion: Union[float, Callable[[float], float]]) -> float:
        if self._value is None:
            return None

        if isinstance(conversion, Callable):
            return conversion(self._value)

        return self._value * conversion

    @property
    def value(self) -> float:
        """Get the value as a float."""
        return self._value
