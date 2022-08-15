import json
import re

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List

from .station import Station
from .string_attribute import StringAttributeMixin
from .time import Time, TimeMixin
from .type import ReportType


class Report(StringAttributeMixin, TimeMixin, metaclass=ABCMeta):
    """Basic structure for an aeronautical report from land stations."""

    def __init__(self, code: str, truncate: bool = False, type: str = "METAR") -> None:
        assert code != "", "code must be a non-empty string"

        code = code.strip()
        self._truncate = truncate

        self._raw_code: str = re.sub(r"\s{2,}|\n+|\t+", " ", code)
        self._raw_code = self._raw_code.replace("=", "")
        self._unparsed_groups: List[str] = []
        self._sections: List[str] = []

        # Initialize mixins
        StringAttributeMixin.__init__(self)
        TimeMixin.__init__(self)

        # Initialize ReportType group
        self._type: ReportType = ReportType(type.upper())

        # Initialize Station group
        self._station: Station = Station(None, None)

    @abstractmethod
    def _handle_sections(self) -> None:
        """Handler to separate the sections of the report."""
        self._sections = []

    def _handle_type(self, match: re.Match) -> None:
        self._type = ReportType(match.string)

        self._concatenate_string(self._type)

    @property
    def type_(self) -> ReportType:
        """Get the type of the report."""
        return self._type

    def _handle_station(self, match: re.Match) -> None:
        self._station = Station(match.string, "ICAO")

        self._concatenate_string(self._station)

    @property
    def station(self) -> Station:
        """Get the station data of the report."""
        return self._station

    @abstractmethod
    def _handle_time(self, match: re.Match) -> None:
        """Hanlder for the time group of the report."""
        pass

    @property
    def time(self) -> Time:
        """Get the time of the report."""
        return self._time

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

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """Returns the report data as a dictionary like `Dict[str, Any]`."""
        return {
            "code": self.raw_code,
            "sections": self.sections,
            "unparsed_groups": self.unparsed_groups,
            "type_": self.type_.as_dict(),
            "station": self.station.as_dict(),
            "time": self.time.as_dict(),
        }

    def to_json(self) -> str:
        """Returns the report data as a string in JSON format."""
        return json.dumps(self.as_dict())
