from abc import ABCMeta, abstractmethod
from typing import Any


class DataDescriptor(metaclass=ABCMeta):
    """Abstract group class for base for aeronautical data."""

    @abstractmethod
    def _handler(self, code: Any):
        """Generate the object to store the relevant data of code."""
        return code

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, code):
        self._value = self._handler(code)
        instance.__dict__[self._name] = self._value


class CodeDescriptor(DataDescriptor):
    def _handler(self, value):
        return value
