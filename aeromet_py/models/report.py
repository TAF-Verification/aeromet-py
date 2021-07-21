from abc import ABCMeta, abstractmethod
from typing import List


class Report(metaclass=ABCMeta):
    """Basic structure of an aeronautical report from land stations"""

    def __init__(self, code: str):
        self.__raw_code = code
        self.__unparsed_groups = []

    @property
    def raw_code(self):
        """Get the raw code as its received in the instance."""
        return self.__raw_code

    @property
    def unparsed_groups(self):
        """Get the unparsed groups of the report."""
        return self.__unparsed_groups

    @property
    @abstractmethod
    def sections(self):
        """Get the report separated in its sections as a list of strings."""

    @abstractmethod
    def _parse(self) -> None:
        """Parse the report to extract relevant data."""
