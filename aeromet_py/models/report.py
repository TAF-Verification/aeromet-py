import re
from abc import ABCMeta, abstractmethod
from typing import List, Any

from .type import Type
from .station import Station


class Report(metaclass=ABCMeta):
    """Basic structure for an aeronautical report from land stations."""

    def __init__(self, code: str, truncate: bool = False) -> None:
        assert code != "", "code must be a non-empty string"

        code = code.strip()
        self._truncate = truncate

        self._raw_code: str = re.sub(r"\s{2,}", " ", code)
        self._raw_code = self._raw_code.replace("=", "")
        self._unparsed_groups: List[str] = []
        self._sections: List[str] = []

        # String buffer
        self._string: str = ""

        # Type group
        self._type: Type = Type("METAR")

        # Station group
        self._station: Station = Station(None, None)

    def __str__(self) -> str:
        return self._string

    def _concatenate_string(self, obj: Any) -> None:
        self._string += str(obj) + "\n"

    @abstractmethod
    def _parse(self) -> None:
        """Parse the report groups to extract relevant data."""
        return None

    @abstractmethod
    def _handle_sections(self) -> None:
        """Handler to separate the sections of the report."""
        self._sections = []

    def _handle_type(self, match: re.Match) -> None:
        self._type = Type(match.string)

        self._concatenate_string(self._type)

    @property
    def type(self) -> Type:
        """Get the type of the report."""
        return self._type

    def _handle_station(self, match: re.Match) -> None:
        self._station = Station(match.string, "ICAO")

        self._concatenate_string(self._station)

    @property
    def station(self) -> Station:
        """Get the station data of the report."""
        return self._station

    @property
    def raw_code(self) -> str:
        """Get the raw code as its received in the instance."""
        return self._raw_code

    @property
    def unparsed_groups(self) -> List[str]:
        """Get the unparsed groups of the report."""
        return self._unparsed_groups

    @property
    def sections(self) -> List[str]:
        """Get the report separated in its sections as a list of strings."""
        return self._sections
