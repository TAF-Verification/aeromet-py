import re
from typing import List

import aeromet_py.models as models


class Metar(models.Report):
    """Parser for METAR code."""
    
    __sections = models.MetarSections()

    def __init__(self, code: str):
        super().__init__(code)
        self.__sections = super().raw_code
    
    @property
    def sections(self) -> List[str]:
        return self.__sections
