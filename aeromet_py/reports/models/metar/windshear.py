import re

from typing import Any, Dict, List, Optional

from ..base import Group, GroupList
from .runway_range import set_runway_name


class MetarWindshearRunway(Group):
    """Basic structure for windshear runways groups in METAR."""

    def __init__(self, match: Optional[re.Match]) -> None:
        if match is None:
            super().__init__(None)

            self._all = None
            self._name = None
        else:
            super().__init__(match.string.replace("_", " "))

            self._all = match.group("all")
            _name: str = match.group("name")
            if _name is None or len(_name) == 2:
                self._name = _name
            elif len(_name) == 3:
                self._name = set_runway_name(_name)
            else:
                self._name = None

    def __str__(self) -> str:
        if self._name:
            return self._name

        if self._all:
            return "all"

        return ""

    @property
    def all_(self) -> bool:
        """Get if `ALL` is found in the group."""
        if self._all:
            return True

        return False

    @property
    def name(self) -> Optional[str]:
        """Get the name of the runway with windshear."""
        return self._name

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "all": self.all_,
            "name": self.name,
        }
        d.update(super().as_dict())
        return d


class MetarWindshearList(GroupList[MetarWindshearRunway]):
    """Basic structure for windshear groups in METAR."""

    def __init__(self) -> None:
        super().__init__(3)

    def __str__(self) -> str:
        if self.all_runways:
            return "all runways"

        return super().__str__()

    @property
    def names(self) -> List[str]:
        """Get the names of runways with windshear reported."""
        if self.all_runways:
            return []

        return [runway.name for runway in self._list]

    @property
    def all_runways(self) -> bool:
        """Get if all runways have windshear."""
        if len(self._list) == 1 and self._list[0].all_:
            return True

        return False
