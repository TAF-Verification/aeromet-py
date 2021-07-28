from .descriptors import DataDescriptor, CodeDescriptor
import re

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


class Visibility:
    
    __code = CodeDescriptor()
    __visibility = VisibilityDescriptor()
    __cavok = CavokDescriptor()
    
    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__visibility = None
            self.__cavok = None
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
    
    def __handle_value(self, transformation):
        if self.__visibility is None:
            return None
        
        return self.__visibility * transformation
    
    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def in_meters(self) -> float:
        return self.__handle_value(1)
    
    @property
    def in_kilometers(self) -> float:
        return self.__handle_value(M_TO_KM)
    
    @property
    def in_sea_miles(self) -> float:
        return self.__handle_value(M_TO_SMI)
    
    @property
    def cavok(self) -> bool:
        return self.__cavok