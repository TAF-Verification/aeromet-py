import re

import aeromet_py.models as models


class Metar:
    """Parser for METAR code."""

    __sections = models.Sections("sections")

    def __init__(self, code: str) -> None:
        self.__raw_code = re.sub(r"\s{2,}", " ", code)
        self.__sections = self.__raw_code
        # self.__code_list = code.split(" ")
        # self.__type = self.__code_list[0]
        # self.__correction = self.__code_list[1]
        # self.__wind = models.Wind(self.__code_list[4])

    @property
    def raw_code(self):
        """The report as raw code."""
        return self._raw_code

    @property
    def sections(self) -> models.Sections:
        """The report divided in its sections."""
        return self.__sections

    # @property
    # def correction(self) -> models.Correction:
    #     """Correction of the report."""
    #     return self.__correction

    # @property
    # def wind(self) -> models.Wind:
    #     return self.__wind
