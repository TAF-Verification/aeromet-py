from abc import ABCMeta
from typing import Generic, List, TypeVar

from .descriptor import DataDescriptor
from .errors import RangeError


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


G = TypeVar("G", bound=Group)


class GroupList(Generic[G]):
    """Basic structure of a groups list from groups found in a aeronautical
    report from land stations."""

    _max_items = DataDescriptor()
    _list = DataDescriptor()

    def __init__(self, max_items: int) -> None:
        self._n = 0
        self._max_items = max_items
        self._list: List[G] = []

    def __str__(self) -> str:
        return " | ".join(str(group) for group in self._list)

    def __iter__(self):
        return self

    def __next__(self) -> G:
        if self._n >= len(self._list):
            self._n = 0
            raise StopIteration

        index = self._n
        self._n += 1
        return self._list[index]

    def __getitem__(self, index: int) -> G:
        if index >= self._max_items:
            raise RangeError(
                f"can't get more than {self._max_items} items in {self.__class__}"
            )
        return self._list[index]

    def __len__(self) -> int:
        return len(self._list)

    def add(self, group: G) -> None:
        """Adds groups to the list."""
        if len(self._list) >= self._max_items:
            raise RangeError(
                f"can't set more than {self._max_items} groups in {self.__class__}"
            )

        self._list.append(group)

    @property
    def codes(self) -> List[str]:
        """Returns the codes of every group found in report as a List[str]."""
        return [group.code for group in self._list]

    @property
    def items(self) -> List[G]:
        """Returns the groups found in report as a List[T]."""
        return self._list
