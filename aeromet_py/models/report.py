import re
from abc import ABCMeta, abstractmethod
from typing import List, Any

from .descriptor import DataDescriptor
from .type import Type
from .station import Station


class Report(metaclass=ABCMeta):
    """Basic structure for an aeronautical report from land stations."""

    _sections = DataDescriptor()

    def __init__(self, code: str):
        assert code != "", "code must be a non-empty string"

        code = code.strip()
        self._raw_code: str = re.sub(r"\s{2,}", " ", code)
        self._unparsed_groups: List[str] = []

        # String buffer
        self._string: str = ""

        # Type group
        self._type: Type = Type("METAR")

        # Station group
        self._station: Station = Station(None)

    def __str__(self) -> str:
        return self._string

    def _concatenate_string(self, object: Any) -> None:
        self._string += str(object) + "\n"

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

    def _handle_type(self, match: re.Match) -> None:
        self._type = Type(match.string)

        self._concatenate_string(self._type)

    @property
    def type(self) -> Type:
        """Returns the type of the report.

        Returns:
            models.Type: the type class.
        """
        return self._type

    def _handle_station(self, match: re.Match) -> None:
        self._station = Station(match.string)

        self._concatenate_string(self._station)

    @property
    def station(self) -> Station:
        """Returns the station data of the report.

        Returns:
            models.Station: the station class.
        """
        return self._station

    @abstractmethod
    def _parse(self) -> None:
        """Parse the report groups to extract relevant data."""
        return None
