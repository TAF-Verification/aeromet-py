import re
from abc import ABCMeta, abstractmethod
from typing import List, Any


class Report(metaclass=ABCMeta):
    """Basic structure for an aeronautical report from land stations."""

    def __init__(self, code: str) -> None:
        assert code != "", "code must be a non-empty string"

        code = code.strip()

        self._raw_code: str = re.sub(r"\s{2,}", " ", code)
        self._raw_code = self._raw_code.replace("=", "")
        self._unparsed_groups: List[str] = []
        self._sections: List[str] = []

        # String buffer
        self._string: str = ""

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
