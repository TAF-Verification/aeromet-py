from abc import ABCMeta
from typing import Callable, Optional, Union


class Numeric(metaclass=ABCMeta):
    """Basic structure to handle numeric values."""

    def __init__(self, value: Optional[float]) -> None:
        self._value = value

    def __str__(self) -> str:
        if self._value is None:
            return ""

        return f"{self._value:.1f}"

    def converted(
        self, conversion: Union[float, Callable[[float], float]]
    ) -> Optional[float]:
        if self._value is None:
            return None

        if isinstance(conversion, Callable):
            return conversion(self._value)

        return self._value * conversion

    @property
    def value(self) -> Optional[float]:
        """Get the value as a float."""
        return self._value
