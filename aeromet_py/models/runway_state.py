import re

from aeromet_py.utils import SkyTranslations

from .descriptors import CodeDescriptor, DataDescriptor
from .visibility import NameDescriptor


class DepositsDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SkyTranslations.RUNWAY_DEPOSITS.get(code)


class ContaminationDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return SkyTranslations.RUNWAY_CONTAMINATION.get(code)


class DepositsDepthDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        try:
            depth = int(code)
        except ValueError:
            pass
        else:
            if depth > 0 and depth <= 90:
                return f"{depth} mm"

        return SkyTranslations.DEPOSIT_DEPTH.get(code)


class SurfaceFrictionDescriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        try:
            coef = int(code)
        except ValueError:
            pass
        else:
            if coef > -1 and coef <= 90:
                return "0.{:02d}".format(coef)

        return SkyTranslations.SURFACE_FRICTION.get(code)


class SNOCLO_Descriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return "aerodrome is closed due to extreme deposit of snow"


class CLRD_Descriptor(DataDescriptor):
    def _handler(self, code):
        if code is None:
            return None

        return "contaminations have ceased to exist"


class RunwayState:

    __code = CodeDescriptor()
    __name = NameDescriptor()
    __deposits = DepositsDescriptor()
    __contamination = ContaminationDescriptor()
    __deposits_depth = DepositsDepthDescriptor()
    __surface_friction = SurfaceFrictionDescriptor()
    __snoclo = SNOCLO_Descriptor()
    __clrd = CLRD_Descriptor()

    def __init__(self, match: re.Match):
        self.__match = match
        if self.__match is None:
            self.__code = None
            self.__name = None
            self.__deposits = None
            self.__contamination = None
            self.__deposits_depth = None
            self.__surface_friction = None
            self.__snoclo = None
            self.__clrd = None
        else:
            self.__code = match.string
            self.__name = match.group("name")
            self.__deposits = match.group("deposit")
            self.__contamination = match.group("contamination")
            self.__deposits_depth = match.group("depth")
            self.__surface_friction = match.group("friction")
            self.__snoclo = match.group("snoclo")
            self.__clrd = match.group("clrd")

    def __deposits_to_str(self):
        deposit = self.__match.group("deposit")
        depth = self.__match.group("depth")

        if deposit == "/":
            if depth == "99" or depth == "//":
                sep = "{} and {}"
            elif depth is not None:
                sep = "depth of {} but {}"
            else:
                return self.deposits
        elif deposit is not None:
            if depth == "99" or depth == "//":
                sep = "{} of {}"
            elif depth is not None:
                sep = "deposits of {} of {}"
            else:
                return "deposits of {}".format(self.deposits)
        else:
            if depth == "99" or depth == "//":
                return self.deposits_depth
            elif depth is not None:
                return "deposits depth of {}".format(self.deposits_depth)
            else:
                return ""

        return sep.format(self.deposits_depth, self.deposits)

    def __surface_friction_to_str(self):
        friction = self.__match.group("friction")

        if friction is not None:
            try:
                friction = int(friction)
            except ValueError:
                return self.surface_friction
            else:
                if friction < 91:
                    return f"estimated surface friction {self.surface_friction}"
                else:
                    return self.surface_friction
        else:
            return ""

    def __str__(self):
        if self.__match is None:
            return ""

        if self.snoclo:
            return self.snoclo

        if self.clrd:
            return self.clrd

        return (
            f"{self.name}, "
            f"{self.__deposits_to_str()}, "
            f"contamination {self.contamination}, "
            f"{self.__surface_friction_to_str()}"
        )

    @property
    def code(self) -> str:
        return self.__code

    @property
    def name(self) -> str:
        return self.__name

    @property
    def deposits(self) -> str:
        return self.__deposits

    @property
    def contamination(self) -> str:
        return self.__contamination

    @property
    def deposits_depth(self) -> str:
        return self.__deposits_depth

    @property
    def surface_friction(self) -> str:
        return self.__surface_friction

    @property
    def snoclo(self) -> str:
        return self.__snoclo

    @property
    def clrd(self) -> str:
        if self.__clrd is None:
            return None

        if self.name == "repeated":
            return self.__clrd + " on previous runway"

        if self.name == "all runways":
            return self.__clrd + f" on {self.name}"

        return self.__clrd + f" on runway {self.name}"
