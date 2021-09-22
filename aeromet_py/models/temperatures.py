import re

from aeromet_py.utils import Conversions, handle_temperature

from .descriptors import CodeDescriptor, DataDescriptor


def set_temperature(sign: str, temp: str):
    if sign == "M" or sign == "-":
        return f"-{temp}"

    return temp


class TemperatureDescriptor(DataDescriptor):
    def _handler(self, value):
        if value is None:
            return None

        try:
            return float(value)
        except ValueError:
            return None


class Temperatures:

    __code = CodeDescriptor()
    __temperature = TemperatureDescriptor()
    __dewpoint = TemperatureDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__temperature = None
            self.__dewpoint = None
        else:
            self.__code = match.string
            self.__temperature = set_temperature(
                match.group("tsign"), match.group("temp")
            )
            self.__dewpoint = set_temperature(
                match.group("dsign"), match.group("dewpt")
            )

    def __str__(self):
        if self.__temperature is None and self.__dewpoint:
            return "no temperature | dewpoint {:.1f}°".format(self.dewpoint_in_celsius)
        elif self.__temperature and self.__dewpoint is None:
            return "temperature {:.1f}° | no dewpoint"
        elif self.__temperature is None and self.__dewpoint is None:
            return ""
        else:
            return "temperature {:.1f}° | dewpoint {:.1f}°".format(
                self.temperature_in_celsius,
                self.dewpoint_in_celsius,
            )

    @property
    def code(self) -> str:
        return self.__code

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

    @property
    def dewpoint_in_celsius(self) -> float:
        return self.__dewpoint

    @property
    def dewpoint_in_fahrenheit(self) -> float:
        return handle_temperature(self.__dewpoint, Conversions.celsius_to_fahrenheit)

    @property
    def dewpoint_in_kelvin(self) -> float:
        return handle_temperature(self.__dewpoint, Conversions.celsius_to_kelvin)

    @property
    def dewpoint_in_rankine(self) -> float:
        return handle_temperature(self.__dewpoint, Conversions.celsius_to_rankine)
