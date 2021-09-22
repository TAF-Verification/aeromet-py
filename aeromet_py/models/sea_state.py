import re

from aeromet_py.utils import Conversions, SkyTranslations, handle_temperature

from .descriptors import CodeDescriptor, DataDescriptor
from .temperatures import TemperatureDescriptor, set_temperature


class StateDescriptor(DataDescriptor):
    def _handler(self, value):
        return SkyTranslations.SEA_STATE.get(value)


class SeaState:

    __code = CodeDescriptor()
    __temperature = TemperatureDescriptor()
    __state = StateDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__temperature = None
            self.__state = None
        else:
            self.__code = match.string
            self.__temperature = set_temperature(
                match.group("sign"), match.group("temp")
            )
            self.__state = match.group("state")

    def __str__(self):
        if self.__temperature is None and self.__state:
            return f"no temperature, {self.state}"
        elif self.__temperature and self.__state is None:
            return "temperature {:.1f}".format(self.temperature_in_celsius)
        elif self.__temperature is None and self.__state is None:
            return ""
        else:
            return "temperature {:.1f}°, {}".format(
                self.temperature_in_celsius,
                self.state,
            )

    @property
    def code(self) -> str:
        return self.__code

    @property
    def state(self) -> str:
        return self.__state

    @property
    def temperature_in_celsius(self) -> float:
        return self.__temperature

    @property
    def temperature_in_fahrenheit(self) -> float:
        return handle_temperature(self.__temperature, Conversions.celsius_to_fahrenheit)

    @property
    def temperature_in_kelvin(self) -> float:
        return handle_temperature(self.__temperature, Conversions.celsius_to_kelvin)

    @property
    def temperature_in_rankine(self) -> float:
        return handle_temperature(self.__temperature, Conversions.celsius_to_rankine)
