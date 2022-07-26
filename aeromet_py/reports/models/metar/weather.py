import re

from typing import Dict, Optional

from ..base import Group, GroupList, HasConcatenateStringProntocol


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
    "NSW": "nil significant weather",
}


class MetarWeather(Group):
    """Basic structure for weather groups in reports from land stations."""

    def __init__(self, match: Optional[re.Match]) -> None:
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

    def __str__(self) -> str:
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
    def intensity(self) -> Optional[str]:
        """Returns the intensity of the weather."""
        return self._intensity

    @property
    def description(self) -> Optional[str]:
        """Returns the description of the weather."""
        return self._description

    @property
    def precipitation(self) -> Optional[str]:
        """Returns the precipitation type of the weather."""
        return self._precipitation

    @property
    def obscuration(self) -> Optional[str]:
        """Returns the obscuration type of the weather."""
        return self._obscuration

    @property
    def other(self) -> Optional[str]:
        """Returns the other parameter of the weather."""
        return self._other

    def as_dict(self) -> Dict[str, Optional[str]]:
        d = {
            "intensity": self.intensity,
            "description": self.description,
            "precipitation": self.precipitation,
            "obscuration": self.obscuration,
            "other": self.other,
        }
        d.update(super().as_dict())
        return d


class MetarWeatherMixin(HasConcatenateStringProntocol):
    """Mixin to add weather list attribute to the report."""

    def __init__(self) -> None:
        self._weathers = GroupList[MetarWeather](3)

    def _handle_weather(self, match: re.Match) -> None:
        weather: MetarWeather = MetarWeather(match)
        self._weathers.add(weather)

        self._concatenate_string(weather)

    @property
    def weathers(self) -> GroupList[MetarWeather]:
        """Get the weather data of the report if provided."""
        return self._weathers
