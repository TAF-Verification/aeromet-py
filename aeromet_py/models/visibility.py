import re

from .descriptors import CodeDescriptor, DataDescriptor
from .wind import COMPASS_DIRS, DEGREES_TO_GRADIANS, DEGREES_TO_RADIANS

SMI_TO_KM = 1.852
KM_TO_SMI = 1 / SMI_TO_KM
KM_TO_M = 1000
M_TO_KM = 1 / KM_TO_M
M_TO_SMI = M_TO_KM * KM_TO_SMI
FT_TO_M = 0.3048
M_TO_FT = 1 / FT_TO_M


class VisibilityDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None
        return float(code)


class CavokDescriptor(DataDescriptor):
    def _handler(self, code):
        if code == "CAVOK":
            return True
        return False


class DirectionDescriptor(DataDescriptor):
    def _handler(self, code):
        return code


def _handle_direction(value, transformation):
    if value is None:
        return None

    if value == "N":
        return 360.0

    values = COMPASS_DIRS[value]

    return sum(values) / 2 * transformation


def _handle_visibility(value, transformation):
    if value is None:
        return None

    return value * transformation


class Visibility:

    __code = CodeDescriptor()
    __visibility = VisibilityDescriptor()
    __cavok = CavokDescriptor()
    __direction = DirectionDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__visibility = None
            self.__cavok = None
            self.__direction = None
        else:
            self.__code = match.string.replace("_", " ")

            if match.group("visextreme") is not None:
                if match.group("visextreme").count("/") > 0:
                    _items = match.group("visextreme").split("/")
                    _visextreme = int(_items[0]) / int(_items[1])
                else:
                    _visextreme = float(match.group("visextreme"))
            else:
                _visextreme = 0

            if match.group("vis") is not None:
                if match.group("vis") == "9999":
                    self.__visibility = 10_000
                else:
                    self.__visibility = match.group("vis")
            elif match.group("opt") is not None:
                _opt = float(match.group("opt"))
                _vis = _opt + _visextreme

                self.__visibility = _vis * SMI_TO_KM * KM_TO_M
            elif match.group("visextreme") is not None:
                self.__visibility = _visextreme * SMI_TO_KM * KM_TO_M
            else:
                self.__visibility = 10_000

            self.__cavok = match.group("cavok")
            self.__direction = match.group("dir")

    def __str__(self):
        if self.__cavok:
            return "Ceiling and Visibility OK"

        return "{} km{}".format(
            self.in_kilometers,
            f" to {self.__direction}" if self.__direction else "",
        )

    @property
    def code(self) -> str:
        return self.__code

    @property
    def in_meters(self) -> float:
        return _handle_visibility(self.__visibility, 1)

    @property
    def in_kilometers(self) -> float:
        return _handle_visibility(self.__visibility, M_TO_KM)

    @property
    def in_sea_miles(self) -> float:
        return _handle_visibility(self.__visibility, M_TO_SMI)

    @property
    def cavok(self) -> bool:
        return self.__cavok

    @cavok.setter
    def cavok(self, value: bool):
        if isinstance(value, bool):
            self.__cavok = value
        else:
            raise TypeError("can't set cavok to {}".format(type(value)))

    @property
    def cardinal_direction(self) -> str:
        return self.__direction

    @property
    def direction_in_degrees(self) -> float:
        return _handle_direction(self.__direction, 1)

    @property
    def direction_in_radians(self) -> float:
        return _handle_direction(self.__direction, DEGREES_TO_RADIANS)

    @property
    def direction_in_gradians(self) -> float:
        return _handle_direction(self.__direction, DEGREES_TO_GRADIANS)


class MinimumVisibility:

    __code = CodeDescriptor()
    __visibility = VisibilityDescriptor()
    __direction = DirectionDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__visibility = None
            self.__direction = None
        else:
            self.__code = match.string
            self.__visibility = match.group("vis")
            self.__direction = match.group("dir")

    def __str__(self):
        if self.__visibility is None:
            return ""

        return "{} km{}".format(
            self.in_kilometers,
            f" to {self.__direction}" if self.__direction else "",
        )

    @property
    def code(self) -> str:
        return self.__code

    @property
    def in_meters(self) -> float:
        return _handle_visibility(self.__visibility, 1)

    @property
    def in_kilometers(self) -> float:
        return _handle_visibility(self.__visibility, M_TO_KM)

    @property
    def in_sea_miles(self) -> float:
        return _handle_visibility(self.__visibility, M_TO_SMI)

    @property
    def cardinal_direction(self) -> str:
        return self.__direction

    @property
    def direction_in_degrees(self) -> float:
        return _handle_direction(self.__direction, 1)

    @property
    def direction_in_radians(self) -> float:
        return _handle_direction(self.__direction, DEGREES_TO_RADIANS)

    @property
    def direction_in_gradians(self) -> float:
        return _handle_direction(self.__direction, DEGREES_TO_GRADIANS)


NAMES = {
    "R": "right",
    "L": "left",
    "C": "center",
}


class NameDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        name_char = code[-1]
        name_str = NAMES.get(name_char, None)

        return code.replace(name_char, f" {name_str}")


LIMITS = {
    "M": "below of",
    "P": "above of",
}


class RVRLimit(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return LIMITS.get(code, None)


TRENDS = {
    "N": "no change",
    "U": "increasing",
    "D": "decreasing",
}


class TrendDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return TRENDS.get(code, None)


class RunwayRange:

    __code = CodeDescriptor()
    __name = NameDescriptor()
    __rvrlow = RVRLimit()
    __low = VisibilityDescriptor()
    __rvrhigh = RVRLimit()
    __high = VisibilityDescriptor()
    __trend = TrendDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__name = None
            self.__rvrlow = None
            self.__low = None
            self.__rvrhigh = None
            self.__high = None
            self.__trend = None
        else:
            units = match.group("units")
            self.__code = match.string
            self.__name = match.group("name")
            self.__rvrlow = match.group("rvrlow")
            self.__rvrhigh = match.group("rvrhigh")
            self.__trend = match.group("trend")

            if units == "FT":
                self.__low = float(match.group("low")) * FT_TO_M

                try:
                    self.__high = float(match.group("high")) * FT_TO_M
                except TypeError:
                    self.__high = match.group("high")
            else:
                self.__low = match.group("low")
                self.__high = match.group("high")

    def __high_as_string(self):
        if self.__high and self.__rvrhigh:
            high = " varying to {} {:.1f} meters".format(self.__rvrhigh, self.__high)
        elif self.__high:
            high = " varying to {:.1f} meters".format(self.__high)
        else:
            high = ""

        return high

    def __str__(self):
        return "runway {} {}{:.1f} meters{}{}".format(
            self.__name,
            self.__rvrlow + " " if self.__rvrlow else "",
            self.__low,
            self.__high_as_string(),
            ", " + self.__trend if self.__trend else "",
        )

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def low_range(self):
        if self.__rvrlow:
            return "{} {:.1f} meters".format(
                self.__rvrlow,
                self.__low,
            )

        return "{:.1f} meters".format(self.__low)

    @property
    def low_in_meters(self):
        return _handle_visibility(self.__low, 1)

    @property
    def low_in_kilometers(self):
        return _handle_visibility(self.__low, M_TO_KM)

    @property
    def low_in_sea_miles(self):
        return _handle_visibility(self.__low, M_TO_SMI)

    @property
    def low_in_feet(self):
        return _handle_visibility(self.__low, M_TO_FT)

    @property
    def high_range(self):
        high = re.sub(r"\svarying\sto\s", "", self.__high_as_string())
        return high

    @property
    def high_in_meters(self):
        return _handle_visibility(self.__high, 1)

    @property
    def high_in_kilometers(self):
        return _handle_visibility(self.__high, M_TO_KM)

    @property
    def high_in_sea_miles(self):
        return _handle_visibility(self.__high, M_TO_SMI)

    @property
    def high_in_feet(self):
        return _handle_visibility(self.__high, M_TO_FT)

    @property
    def trend(self):
        return self.__trend
