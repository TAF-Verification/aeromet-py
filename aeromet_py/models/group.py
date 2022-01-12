from abc import ABCMeta


class Group(metaclass=ABCMeta):
    """Basic structure of a group in a aeronautical report from land stations."""

    def __init__(self, code: str) -> None:
        self._code = code

    def __str__(self) -> str:
        return str(self._code)

    def __len__(self) -> int:
        if self._code is None:
            return 0

        return len(self._code)

    @property
    def code(self) -> str:
        """Get the code of the group."""
        return self._code
