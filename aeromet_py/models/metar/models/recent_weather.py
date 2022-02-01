import re

from ...group import Group
from .weather import DESCRIPTION, OBSCURATION, OTHER, PRECIPITATION


class MetarRecentWeather(Group):
    """Basic structure for recent weather groups in METAR."""

    def __init__(self, match: re.Match) -> None:
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

    def __str__(self):
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
    def description(self) -> str:
        """Get the description of recent weather in METAR."""
        return self._description

    @property
    def obscuration(self) -> str:
        """Get the obscuration of recent weather in METAR."""
        return self._obscuration

    @property
    def other(self) -> str:
        """Get the other item of recent weather in METAR."""
        return self._other

    @property
    def precipitation(self) -> str:
        """Get the precipitation of recent weather in METAR."""
        return self._precipitation
