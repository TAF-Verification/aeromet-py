import re
from typing import Dict

from ...group import Group

INTENSITY: Dict[str, str] = {
    "-": "light",
    "+": "heavy",
    "-VC": "nearby light",
    "+VC": "nearby heavy",
    "VC": "nearby",
}

DESCRIPTION: Dict[str, str] = {
    "MI": "shallow",
    "PR": "partial",
    "BC": "patches of",
    "DR": "low drifting",
    "BL": "blowing",
    "SH": "showers",
    "TS": "thunderstorm",
    "FZ": "freezing",
}

PRECIPITATION: Dict[str, str] = {
    "DZ": "drizzle",
    "RA": "rain",
    "SN": "snow",
    "SG": "snow grains",
    "IC": "ice crystals",
    "PL": "ice pellets",
    "GR": "hail",
    "GS": "snow pellets",
    "UP": "unknown precipitation",
    "//": "",
}

OBSCURATION: Dict[str, str] = {
    "BR": "mist",
    "FG": "fog",
    "FU": "smoke",
    "VA": "volcanic ash",
    "DU": "dust",
    "SA": "sand",
    "HZ": "haze",
    "PY": "spray",
}

OTHER: Dict[str, str] = {
    "PO": "sand whirls",
    "SQ": "squalls",
    "FC": "funnel cloud",
    "SS": "sandstorm",
    "DS": "dust storm",
}


class MetarWeather(Group):
    """Basic structure for weather groups in reports from land stations."""

    def __init__(self, match: re.Match) -> None:
        if match is None:
            super().__init__(None)

            self._intensity = None
            self._description = None
            self._precipitation = None
            self._obscuration = None
            self._other = None
        else:
            super().__init__(match.string)

            self._intensity = INTENSITY.get(match.group("int"), None)
            self._description = DESCRIPTION.get(match.group("desc"), None)
            self._precipitation = PRECIPITATION.get(match.group("prec"), None)
            self._obscuration = OBSCURATION.get(match.group("obsc"), None)
            self._other = OTHER.get(match.group("other"), None)

    def __str__(self):
        s = "{} {} {} {} {}".format(
            self._intensity,
            self._description,
            self._precipitation,
            self._obscuration,
            self._other,
        )
        s = s.replace("None", "")
        s = re.sub(r"\s{2,}", " ", s)

        return s.strip()

    @property
    def intensity(self) -> str:
        """Returns the intensity of the weather."""
        return self._intensity

    @property
    def description(self) -> str:
        """Returns the description of the weather."""
        return self._description

    @property
    def precipitation(self) -> str:
        """Returns the precipitation type of the weather."""
        return self._precipitation

    @property
    def obscuration(self) -> str:
        """Returns the obscuration type of the weather."""
        return self._obscuration

    @property
    def other(self) -> str:
        """Returns the other parameter of the weather."""
        return self._other
