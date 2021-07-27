import re
from math import pi

from .descriptors import CodeDescriptor, DataDescriptor

COMPASS_DIRS = {
    "NNE": [11.25, 33.75],
    "NE": [33.75, 56.25],
    "ENE": [56.25, 78.75],
    "E": [78.75, 101.25],
    "ESE": [101.25, 123.75],
    "SE": [123.75, 146.25],
    "SSE": [146.25, 168.75],
    "S": [168.75, 191.25],
    "SSW": [191.25, 213.75],
    "SW": [213.75, 236.25],
    "WSW": [236.25, 258.75],
    "W": [258.75, 281.25],
    "WNW": [281.25, 303.75],
    "NW": [303.75, 326.25],
    "NNW": [326.25, 348.75],
    "N": [348.75, 11.25],
}

DEGREES_TO_RADIANS = pi / 180
DEGREES_TO_GRADIANS = 1.11111111
KNOT_TO_MPS = 0.51444444
KNOT_TO_MIPH = 1.15078
KNOT_TO_KPH = 1.852
MPS_TO_KNOT = 1 / KNOT_TO_MPS


class DirectionDescriptor(DataDescriptor):
    def _handler(self, value):
        if value is None:
            return None

        try:
            return float(value)
        except ValueError:
            return value


class SpeedDescriptor(DataDescriptor):
    def _handler(self, value):
        if value is None:
            return None

        try:
            return float(value)
        except ValueError:
            return value


class WindVariation:

    __code = CodeDescriptor()
    __from = DirectionDescriptor()
    __to = DirectionDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__from = None
            self.__to = None
        else:
            self.__code = match.string
            self.__from = match.group("from")
            self.__to = match.group("to")

    def __str__(self):
        return "from {} ({:.1f}°) to {} ({:.1f}°)".format(
            self.from_cardinal_direction,
            self.__from,
            self.to_cardinal_direction,
            self.__to,
        )

    def __handle_cardinal(self, value):
        dirs = COMPASS_DIRS["N"]
        if value >= dirs[0] or value < dirs[1]:
            return "N"

        for k, v in COMPASS_DIRS.items():
            if value >= v[0] and value < v[1]:
                return k

        return None

    @property
    def code(self) -> str:
        return self.__code

    @property
    def from_cardinal_direction(self) -> str:
        return self.__handle_cardinal(self.__from)

    @property
    def from_in_degrees(self) -> float:
        return self.__from

    @property
    def from_in_radians(self) -> float:
        return self.__from * DEGREES_TO_RADIANS

    @property
    def from_in_gradians(self) -> float:
        return self.__from * DEGREES_TO_GRADIANS

    @property
    def to_cardinal_direction(self) -> str:
        return self.__handle_cardinal(self.__to)

    @property
    def to_in_degrees(self) -> float:
        return self.__to

    @property
    def to_in_radians(self) -> float:
        return self.__to * DEGREES_TO_RADIANS

    @property
    def to_in_gradians(self) -> float:
        return self.__to * DEGREES_TO_GRADIANS


class Wind:

    __code = CodeDescriptor()
    __direction = DirectionDescriptor()
    __speed = SpeedDescriptor()
    __gust = SpeedDescriptor()

    def __init__(self, match: re.Match):
        if match is None:
            self.__code = None
            self.__direction = None
            self.__speed = None
            self.__gust = None
        else:
            self.__code = match.string
            self.__units = match.group("units")
            self.__direction = match.group("dir")

            if self.__units == "KT":
                self.__speed = match.group("speed")
                self.__gust = match.group("gust")

            if self.__units == "MPS":
                speed = match.group("speed")
                gust = match.group("gust")

                try:
                    self.__speed = "{}".format(float(speed) * MPS_TO_KNOT)
                except (TypeError, ValueError):
                    self.__speed = speed

                try:
                    self.__gust = "{}".format(float(gust) * MPS_TO_KNOT)
                except (TypeError, ValueError):
                    self.__gust = gust

    def __str__(self):
        gust = (
            ""
            if self.__gust is None
            else " gusts of {:.1f} kt".format(self.gust_in_knot)
        )
        return "{} ({:.1f}°) {:.1f} kt{}".format(
            self.cardinal_direction,
            self.__direction,
            self.speed_in_knot,
            gust,
        )

    @property
    def code(self) -> str:
        return self.__code

    def __handle_value(self, value, transformation):
        if value is None:
            return None

        if isinstance(value, str):
            if value == "VRB":
                return "variable"
            elif value in ["///", "//"]:
                return None
            else:
                return value

        return value * transformation

    @property
    def cardinal_direction(self) -> str:
        value = self.__handle_value(self.__direction, 1)

        if isinstance(value, float):
            dirs = COMPASS_DIRS["N"]
            if value >= dirs[0] or value < dirs[1]:
                return "N"

            for k, v in COMPASS_DIRS.items():
                if value >= v[0] and value < v[1]:
                    return k

        return None

    @property
    def direction_in_degrees(self) -> float:
        return self.__handle_value(self.__direction, 1)

    @property
    def direction_in_radians(self) -> float:
        return self.__handle_value(self.__direction, DEGREES_TO_RADIANS)

    @property
    def direction_in_gradians(self) -> float:
        return self.__handle_value(self.__direction, DEGREES_TO_GRADIANS)

    @property
    def speed_in_mps(self) -> float:
        return self.__handle_value(self.__speed, KNOT_TO_MPS)

    @property
    def speed_in_knot(self) -> float:
        return self.__handle_value(self.__speed, 1)

    @property
    def speed_in_kph(self) -> float:
        return self.__handle_value(self.__speed, KNOT_TO_KPH)

    @property
    def speed_in_miph(self) -> float:
        return self.__handle_value(self.__speed, KNOT_TO_MIPH)

    @property
    def gust_in_mps(self) -> float:
        return self.__handle_value(self.__gust, KNOT_TO_MPS)

    @property
    def gust_in_knot(self) -> float:
        return self.__handle_value(self.__gust, 1)

    @property
    def gust_in_kph(self) -> float:
        return self.__handle_value(self.__gust, KNOT_TO_KPH)

    @property
    def gust_in_miph(self) -> float:
        return self.__handle_value(self.__gust, KNOT_TO_MIPH)
