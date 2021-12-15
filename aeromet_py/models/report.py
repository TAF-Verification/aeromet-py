import re
from abc import ABCMeta, abstractmethod
from typing import List

from .descriptor import DataDescriptor


class Report(metaclass=ABCMeta):
    """Basic structure for an aeronautical report from land stations.

    Args:
        metaclass (ABCMeta, optional): This makes Report a metaclass. Defaults to ABCMeta.
    """

    _sections = DataDescriptor()

    def __init__(self, code: str):
        assert code != "", "code must be a non-empty string"

        code = code.strip()
        self._raw_code: str = re.sub(r"\s{2,}", " ", code)
        self._unparsed_groups: List[str] = []

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
    def _parse(self) -> None:
        """Parse the report groups to extract relevant data."""
        return None
