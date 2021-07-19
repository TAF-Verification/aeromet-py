from abc import ABCMeta, abstractmethod
from typing import List


class Report(metaclass=ABCMeta):
    """Basic structure of an aeronautical report from land stations"""
    
    def __init__(self, code: str):
        self.__raw_code = code
    
    @property
    def raw_code(self) -> str:
        """Get the raw code as its received in the instance."""
        return self.__raw_code
    
    @property
    @abstractmethod
    def sections(self) -> List[str]:
        """Get the report separated in its sections as a list of strings."""