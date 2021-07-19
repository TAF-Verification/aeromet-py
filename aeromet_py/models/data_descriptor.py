from abc import ABCMeta, abstractmethod


class DataDescriptor(metaclass=ABCMeta):
    """Abstract data class for base for aeronautical data."""
    
    def __set_name__(self, owner, name):
        self._name = name

    @abstractmethod
    def _handler(self, code: str):
        """Handle the code to extract relevant data."""
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        self._value = self._handler(value)
        instance.__dict__[self._name] = self._value
