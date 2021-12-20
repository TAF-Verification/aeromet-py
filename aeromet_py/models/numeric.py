from typing import Callable, Union
from abc import ABCMeta

from .descriptor import DataDescriptor


class Numeric(metaclass=ABCMeta):

    _value = DataDescriptor()

    def __init__(self, value: float) -> None:
        self._value = value

    def __str__(self) -> str:
        if self._value is None:
            return ""
        return f"{self._value:.1f}"

    def converted(self, conversion: Union[float, Callable]) -> float:
        if self.value is None:
            return None

        if isinstance(conversion, Callable):
            return conversion(self.value)

        return self.value * conversion

    @property
    def value(self) -> float:
        """Returns the value as a float.

        Returns:
            float: the value.
        """
        return self._value
