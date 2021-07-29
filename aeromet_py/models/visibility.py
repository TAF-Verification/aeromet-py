import re

from .descriptors import CodeDescriptor, DataDescriptor
from .wind import COMPASS_DIRS, DEGREES_TO_RADIANS, DEGREES_TO_GRADIANS

SMI_TO_KM = 1.852
KM_TO_SMI = 1 / SMI_TO_KM
KM_TO_M = 1000
M_TO_KM = 1 / KM_TO_M
M_TO_SMI = M_TO_KM * KM_TO_SMI


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