import re
from typing import Dict

from aeromet_py.utils import Conversions

from .descriptor import DataDescriptor
from .group import Group, GroupList
from .visibility import Distance

SKY_COVER: Dict[str, str] = {
    "SKC": "clear",
    "CLR": "clear",
    "NSC": "clear",
    "NCD": "clear",
    "FEW": "a few",
    "SCT": "scattered",
    "BKN": "broken",
    "OVC": "overcast",
    "///": "undefined",
    "VV": "indefinite ceiling",
}

CLOUD_TYPE: Dict[str, str] = {
    "AC": "altocumulus",
    "ACC": "altocumulus castellanus",
    "ACSL": "standing lenticulas altocumulus",
    "AS": "altostratus",
    "CB": "cumulonimbus",
    "CBMAM": "cumulonimbus mammatus",
    "CCSL": "standing lenticular cirrocumulus",
    "CC": "cirrocumulus",
    "CI": "cirrus",
    "CS": "cirrostratus",
    "CU": "cumulus",
    "NS": "nimbostratus",
    "SC": "stratocumulus",
    "ST": "stratus",
    "SCSL": "standing lenticular stratocumulus",
    "TCU": "towering cumulus",
}


class CloudLayer(Group):

    _cover = DataDescriptor()
    _height = DataDescriptor()
    _type = DataDescriptor()
    _oktas = DataDescriptor()

    def __init__(self, match: re.Match) -> None:
        self._oktas: str = "0"

        if match is None:
            super().__init__(None)

            self._height = Distance(None)
        else:
            super().__init__(match.string)

            cover: str = match.group("cover")

            self._set_oktas(cover)

            self._cover = SKY_COVER.get(cover, None)
            self._type = CLOUD_TYPE.get(match.group("type"), None)

            self._set_height(match.group("height"))

    def __str__(self):
        if self._type and self._height.value:
            return "{} at {:.1f} feet of {}".format(
                self._cover,
                self.height_in_feet,
                self._type,
            )

        if self._height.value:
            return "{} at {:.1f} feet".format(
                self._cover,
                self.height_in_feet,
            )

        if self._cover in [SKY_COVER[item] for item in ["NSC", "NCD", "///"]]:
            return self._cover

        if self._cover == SKY_COVER["VV"]:
            if self._height.value:
                return self._cover + f" at {self.height_in_feet} feet"
            return self._cover

        return "{} at undefined height", format(
            self._cover,
        )

    def _set_oktas(self, code: str) -> None:
        if code == "FEW":
            self._oktas = "1-2"

        if code == "SCT":
            self._oktas = "3-4"

        if code == "BKN":
            self._oktas = "5-7"

        if code == "OVC":
            self._oktas = "8"

        if code in ["NSC", "NCD"]:
            self._oktas = "not specified"

        if code in ["///", "VV"]:
            self._oktas = "undefined"

    def _set_height(self, height: str) -> None:
        if height == "///":
            self._height = Distance(None)
        else:
            _height: float = float(height + "00")
            _height = _height * Conversions.FT_TO_M
            self._height = Distance(f"{_height}")

    @property
    def cover(self) -> str:
        """Returns the cover description of the cloud layer."""
        return self._cover

    @property
    def cloud_type(self) -> str:
        """Returns the cloud type of the layer."""
        return self._type

    @property
    def oktas(self) -> str:
        """Returns the oktas amount of the cloud layer."""
        return self._oktas

    @property
    def height_in_meters(self) -> float:
        """Returns the height of the cloud base in meters."""
        return self._height.value

    @property
    def height_in_kilometers(self) -> float:
        """Returns the height of the cloud base in kilometers."""
        return self._height.converted(Conversions.M_TO_KM)

    @property
    def height_in_sea_miles(self) -> float:
        """Returns the height of the cloud base in sea miles."""
        return self._height.converted(Conversions.M_TO_SMI)

    @property
    def height_in_feet(self) -> float:
        """Returns the height of the cloud base in feet."""
        return self._height.converted(Conversions.M_TO_FT)


class CloudList(GroupList[CloudLayer]):
    def __init__(self) -> None:
        super().__init__(4)

    @property
    def ceiling(self) -> bool:
        """Returns True if there is ceiling, False if not.

        If the cover of someone of the cloud layers is broken and its height
        is less or equal than 1500.0 feet, there is ceiling; there isn't
        otherwise."""
        for group in self._list:
            _oktas: str = group.oktas
            _height: float = group.height_in_feet
            if _oktas in ["5-7", "8"] and _height <= 1500.0:
                return True
        return False
