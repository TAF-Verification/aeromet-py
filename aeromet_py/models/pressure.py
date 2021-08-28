import re

from .descriptors import CodeDescriptor, DataDescriptor
from aeromet_py.utils import Conversions, handle_value

class PressureDescriptor(DataDescriptor):
    def _handler(self, value):
        if value is None:
            return None
        
        try:
            return float(value)
        except ValueError:
            return None


class Pressure:
    
    __code = CodeDescriptor()
    __pressure = PressureDescriptor()
    
    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__pressure = None
        else:
            self.__code = match.string
            
            units = match.group('units')
            units2 = match.group('units2')
            value = match.group('press')
            
            if value != '////':
                value = float(value)
                
                if units == 'A' or units2 == 'INS':
                    self.__pressure = value / 100.0 * Conversions.INHG_TO_HPA
                elif units in ['Q', 'QNH']:
                    self.__pressure = value
                elif value > 2500.0:
                    self.__pressure = value * Conversions.INHG_TO_HPA
                else:
                    self.__pressure = value * Conversions.MBAR_TO_HPA
            else:
                self.__pressure = None
    
    def __str__(self):
        return "{:.2f} hPa".format(self.in_hecto_pascals)

    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def in_hecto_pascals(self) -> float:
        return self.__pressure
    
    @property
    def in_mercury_inches(self) -> float:
        return handle_value(self.__pressure, Conversions.HPA_TO_INHG)
    
    @property
    def in_milli_bars(self) -> float:
        return handle_value(self.__pressure, Conversions.HPA_TO_MBAR)
    
    @property
    def in_bars(self) -> float:
        return handle_value(self.__pressure, Conversions.HPA_TO_BAR)
    
    @property
    def in_atmospheres(self) -> float:
        return handle_value(self.__pressure, Conversions.HPA_TO_ATM)