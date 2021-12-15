class DataDescriptor:
    """Abstract data class for base for aeronautical data."""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
