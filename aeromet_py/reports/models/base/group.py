import json

from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, Dict, Generic, List, Optional, TypeVar

from .errors import RangeError


GroupHandler = namedtuple("GroupHandler", "regexp handler")


class Group(metaclass=ABCMeta):
    """Basic structure of a group in a aeronautical report from land stations."""

    def __init__(self, code: Optional[str]) -> None:
        if code is not None:
            code = code.replace("_", " ")
        self._code = code

    def __str__(self) -> str:
        if self._code is not None:
            return str(self._code)

        return ""

    def __len__(self) -> int:
        if self._code is None:
            return 0

        return len(self._code)

    @property
    def code(self) -> Optional[str]:
        """Get the code of the group."""
        return self._code

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """Returns the object data as a dictionary like `Dict[str, Any]`."""
        return {"code": self.code}

    def to_json(self) -> str:
        """Returns the object data as a string in JSON format."""
        return json.dumps(self.as_dict())


G = TypeVar("G", bound=Group)


class GroupList(Generic[G]):
    """Basic structure of a groups list from groups found in a aeronautical
    report from land stations."""

    def __init__(self, max_items: int) -> None:
        self._n = 0
        self._max_items = max_items
        self._list: List[G] = []

    def __str__(self) -> str:
        return " | ".join(str(group) for group in self._list)

    def __iter__(self) -> "GroupList[G]":
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
        """Returns the groups found in report as a List[G]."""
        return self._list

    def as_dict(self) -> Dict[str, Any]:
        """Returns the items data as a dictionary like `Dict[str, Any]`."""
        d = {}
        labels = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "nineth",
            "tenth",
        ]
        for i, obj in enumerate(self._list):
            d[f"{labels[i]}"] = obj.as_dict()

        return d

    def to_json(self) -> str:
        """Returns the items data as a string in JSON format."""
        return json.dumps(self.as_dict())
