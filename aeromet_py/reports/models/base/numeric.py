import json

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Optional


class Numeric(metaclass=ABCMeta):
    """Basic structure to handle numeric values."""

    def __init__(self, value: Optional[float]) -> None:
        self._value = value

    def __str__(self) -> str:
        if self._value is None:
            return ""

        return f"{self._value:.1f}"

    def converted(
        self,
        factor: Optional[float] = None,
        conversion: Optional[Callable[[float], float]] = None,
    ) -> Optional[float]:
        """Returns the value converted to other units defined by
        `factor` or `conversion`. If both are provided, `factor`
        takes precedence.

        Args:
            factor (float | None): the factor to multiply by. Defaults to None.
            conversion (Callable[[float], float] | None): the conversion function. Defaults to None.

        Returns:
            float | None: the value converted to other units. If value is None, returns None.
        """
        if self._value is None:
            return None

        if factor:
            return self._value * factor

        if conversion:
            return conversion(self._value)

        return None

    @property
    def value(self) -> Optional[float]:
        """Get the value as a float."""
        return self._value

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """Returns the numeric value data as a dictionary like `Dict[str, Any]`."""
        raise NotImplementedError()

    def to_json(self) -> str:
        """Returns the object data as a string in JSON format."""
        return json.dumps(self.as_dict())
