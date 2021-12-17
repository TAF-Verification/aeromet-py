from abc import ABCMeta

from .descriptor import DataDescriptor


class Group(metaclass=ABCMeta):
    """Basic structure of a group in a aeronautical report from land stations."""

    _code = DataDescriptor()

    def __init__(self, code: str) -> None:
        self._code = code

    @property
    def code(self) -> str:
        """Returns the code of the group

        Returns:
            str: the code.
        """
        return self._code
