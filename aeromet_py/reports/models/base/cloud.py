import re

from typing import Any, Dict, Optional, Type, TypeVar

from ....utils import Conversions
from .distance import Distance
from .group import Group, GroupList
from .string_attribute import HasConcatenateStringProntocol


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


def _set_oktas(code: str) -> str:
    if code == "FEW":
        return "1-2"

    if code == "SCT":
        return "3-4"

    if code == "BKN":
        return "5-7"

    if code == "OVC":
        return "8"

    if code in ["NSC", "NCD"]:
        return "not specified"

    return "undefined"


C = TypeVar("C", bound="Cloud")


class Cloud(Group):
    """Basic structure for cloud layer groups in reports from land stations.
    To instantiate an object it needs a Dict[str, str] with the following keys:
        * code
        * cover
        * oktas
        * type
        * height
    """

    def __init__(self, data: Dict[str, str]) -> None:
        super().__init__(data.get("code"))

        self._cover = data.get("cover")
        self._oktas = data.get("oktas")
        self._type = data.get("type")
        self._height = Distance(data.get("height"))

    @classmethod
    def from_metar(cls: Type[C], match: Optional[re.Match]) -> C:
        """Classmethod to create a Cloud object from a METAR group."""

        _code: str = None
        _cover: str = None
        _oktas: str = None
        _type: str = None
        _height: str = None

        if match is not None:
            _code = match.string
            cover: str = match.group("cover")

            _cover = SKY_COVER.get(cover, None)
            _oktas = _set_oktas(cover)
            _type = CLOUD_TYPE.get(match.group("type"), None)

            height: str = match.group("height")
            if height is None or height == "///":
                _height = "////"
            else:
                height += "00"
                height_as_float: float = float(height)
                height_as_float = height_as_float * Conversions.FT_TO_M
                _height = f"{height_as_float:.10f}"

        return cls(
            {
                "code": _code,
                "cover": _cover,
                "oktas": _oktas,
                "type": _type,
                "height": _height,
            }
        )

    def __str__(self) -> str:
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

        return "{} at undefined height".format(
            self._cover,
        )

    @property
    def cover(self) -> Optional[str]:
        """Returns the cover description of the cloud layer."""
        return self._cover

    @property
    def cloud_type(self) -> Optional[str]:
        """Returns the type of cloud translation of the cloud layer."""
        return self._type

    @property
    def oktas(self) -> str:
        """Returns the oktas amount of the cloud layer."""
        return self._oktas

    @property
    def height_in_meters(self) -> Optional[float]:
        """Returns the height of the cloud base in meters."""
        return self._height.in_meters

    @property
    def height_in_kilometers(self) -> Optional[float]:
        """Returns the height of the cloud base in kilometers."""
        return self._height.in_kilometers

    @property
    def height_in_sea_miles(self) -> Optional[float]:
        """Returns the height of the cloud base in sea miles."""
        return self._height.in_sea_miles

    @property
    def height_in_feet(self) -> Optional[float]:
        """Returns the height of the cloud base in feet."""
        return self._height.in_feet

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "cover": self.cover,
            "oktas": self.oktas,
            "height_units": "meters",
            "height": self.height_in_meters,
            "type": self.cloud_type,
        }
        d.update(super().as_dict())
        return d


class CloudList(GroupList[Cloud]):
    def __init__(self) -> None:
        super().__init__(4)

    @property
    def ceiling(self) -> bool:
        """Returns True if there is ceiling, False if not.
        If the cover of someone of the cloud layers is broken (BKN) or
        overcast (OVC) and its height is less than or equal to 1500.0 feet,
        there is ceiling; there isn't otherwise."""
        for group in self._list:
            _oktas: str = group.oktas
            _height: float = group.height_in_feet
            if _oktas in ["5-7", "8"] and _height <= 1500.0:
                return True
        return False
