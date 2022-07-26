import re

from typing import Dict, Optional

from ..base import Group
from .weather import DESCRIPTION, OBSCURATION, OTHER, PRECIPITATION


class MetarRecentWeather(Group):
    """Basic structure for recent weather groups in METAR."""

    def __init__(self, match: Optional[re.Match]) -> None:
        if match is None:
            super().__init__(None)

            self._description = None
            self._obscuration = None
            self._other = None
            self._precipitation = None
        else:
            super().__init__(match.string)

            self._description = DESCRIPTION.get(match.group("desc"), None)
            self._obscuration = OBSCURATION.get(match.group("obsc"), None)
            self._other = OTHER.get(match.group("other"), None)
            self._precipitation = PRECIPITATION.get(match.group("prec"), None)

    def __str__(self) -> str:
        s = "{} {} {} {}".format(
            self._description,
            self._precipitation,
            self._obscuration,
            self._other,
        )
        s = s.replace("None", "")
        s = re.sub(r"\s{2,}", " ", s)

        return s.strip()

    @property
    def description(self) -> Optional[str]:
        """Get the description of recent weather in METAR."""
        return self._description

    @property
    def obscuration(self) -> Optional[str]:
        """Get the obscuration of recent weather in METAR."""
        return self._obscuration

    @property
    def other(self) -> Optional[str]:
        """Get the other item of recent weather in METAR."""
        return self._other

    @property
    def precipitation(self) -> Optional[str]:
        """Get the precipitation of recent weather in METAR."""
        return self._precipitation

    def as_dict(self) -> Dict[str, Optional[str]]:
        d = {
            "description": self.description,
            "obscuration": self.obscuration,
            "other": self.other,
            "precipitation": self.precipitation,
        }
        d.update(super().as_dict())
        return d
