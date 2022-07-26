import re

from typing import Any, Dict, Optional

from ..base import Group
from .runway_range import set_runway_name


# Table 0919
RUNWAY_DEPOSITS: Dict[str, str] = {
    "0": "clear and dry",
    "1": "damp",
    "2": "wet and water patches",
    "3": "rime and frost covered (depth normally less than 1 mm)",
    "4": "dry snow",
    "5": "wet snow",
    "6": "slush",
    "7": "ice",
    "8": "compacted or rolled snow",
    "9": "frozen ruts or ridges",
    "/": "type of deposit not reported (e.g. due to runway clearance in progress)",
}

# Table 0519
RUNWAY_CONTAMINATION: Dict[str, str] = {
    "1": "less than 10% of runway",
    "2": "11%-25% of runway",
    "3": "reserved",
    "4": "reserved",
    "5": "26%-50% of runway",
    "6": "reserved",
    "7": "reserved",
    "8": "reserved",
    "9": "51%-100% of runway",
    "/": "not reported",
}

# Table 1079
DEPOSIT_DEPTH: Dict[str, str] = {
    "00": "less than 1 mm",
    "91": "reserved",
    "92": "10 cm",
    "93": "15 cm",
    "94": "20 cm",
    "95": "25 cm",
    "96": "30 cm",
    "97": "35 cm",
    "98": "40 cm or more",
    "99": "runway(s) non-operational due to snow, slush, ice, large drifts or runway clearance, but depth not reported",
    "//": "depth of deposit operationally not significant or not measurable",
}

# Table 0366
SURFACE_FRICTION: Dict[str, str] = {
    "91": "breaking action poor",
    "92": "breaking action medium/poor",
    "93": "breaking action medium",
    "94": "breaking action medium/good",
    "95": "breaking action good",
    "96": "reserved",
    "97": "reserved",
    "98": "reserved",
    "99": "breaking action unreliable",
    "//": "breaking conditions not reported and/or runway not operational",
}


class MetarRunwayState(Group):
    """Basic structure for runway state groups in METAR."""

    def __init__(self, match: Optional[re.Match]) -> None:
        self._snoclo: bool = False
        self._clrd: bool = False
        self._match = match

        if match is None:
            super().__init__(None)

            self._name = None
            self._deposits = None
            self._contamination = None
            self._deposits_depth = None
            self._surface_friction = None
        else:
            super().__init__(match.string)

            self._name = set_runway_name(match.group("name"))
            self._deposits = RUNWAY_DEPOSITS.get(match.group("deposit"), None)
            self._contamination = RUNWAY_CONTAMINATION.get(match.group("cont"), None)
            self._deposits_depth = self._set_deposits_depth(match.group("depth"))
            self._surface_friction = self._set_surface_friction(match.group("fric"))
            self._snoclo = match.group("snoclo") != None
            self._clrd = match.group("clrd") != None

    def _set_deposits_depth(self, code: Optional[str]) -> Optional[str]:
        """Helper to set the deposits type."""
        if code is None:
            return None

        depth: int
        try:
            depth = int(code)
        except ValueError:
            pass
        else:
            if depth > 0 and depth <= 90:
                return f"{depth} mm"

        return DEPOSIT_DEPTH.get(code, None)

    def _set_surface_friction(self, code: Optional[str]) -> Optional[str]:
        """Helper to set the surface friction."""
        if code is None:
            return None

        coef: int
        try:
            coef = int(code)
        except ValueError:
            pass
        else:
            if coef > -1 and coef <= 90:
                return "0.{:02d}".format(coef)

        return SURFACE_FRICTION.get(code, None)

    def _deposits_to_str(self) -> str:
        """Helper to convert deposits to string."""
        deposit = self._match.group("deposit")
        depth = self._match.group("depth")

        if deposit == "/":
            if depth == "99" or depth == "//":
                sep = "{} and {}"
            elif depth is not None:
                sep = "depth of {} but {}"
            else:
                return self._deposits
        elif deposit is not None:
            if depth == "99" or depth == "//":
                sep = "{} of {}"
            elif depth is not None:
                sep = "deposits of {} of {}"
            else:
                return "deposits of {}".format(self._deposits)
        else:
            if depth == "99" or depth == "//":
                return self._deposits_depth
            elif depth is not None:
                return "deposits depth of {}".format(self._deposits_depth)
            else:
                return ""

        return sep.format(self._deposits_depth, self._deposits)

    def _surface_friction_to_str(self) -> str:
        """Helper to convert the surface friction to string."""
        friction = self._match.group("fric")

        if friction is not None:
            try:
                friction = int(friction)
            except ValueError:
                return self._surface_friction
            else:
                if friction < 91:
                    return f"estimated surface friction {self._surface_friction}"
                else:
                    return self._surface_friction
        else:
            return ""

    def __str__(self) -> str:
        if self._match is None:
            return ""

        if self.snoclo:
            return "aerodrome is closed due to extreme deposit of snow"

        if self.clrd:
            return self.clrd

        return (
            f"{self._name}, "
            f"{self._deposits_to_str()}, "
            f"contamination {self._contamination}, "
            f"{self._surface_friction_to_str()}"
        )

    @property
    def name(self) -> Optional[str]:
        """Get the name of the runway."""
        return self._name

    @property
    def deposits(self) -> Optional[str]:
        """Get the deposits type on the runway."""
        return self._deposits

    @property
    def contamination(self) -> Optional[str]:
        """Get the contamination quantity of the deposits."""
        return self._contamination

    @property
    def deposits_depth(self) -> Optional[str]:
        """Get the deposits depth."""
        return self._deposits_depth

    @property
    def surface_friction(self) -> Optional[str]:
        """Get the surface friction index of the runway."""
        return self._surface_friction

    @property
    def snoclo(self) -> bool:
        """
        True: aerodrome is closed due to extreme deposit of snow.
        False: aerodrome is open.
        """
        return self._snoclo

    @property
    def clrd(self) -> Optional[str]:
        """Get if contamination have ceased to exists in some runway as string."""
        clrd_text: str = "contaminations have ceased to exists"

        if not self._clrd:
            return None

        if self._name == "repeated":
            return clrd_text + " on previous runway"

        if self._name == "all runways":
            return clrd_text + f" on {self._name}"

        return clrd_text + f" on runway {self.name}"

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "name": self.name,
            "deposits": self.deposits,
            "contamination": self.contamination,
            "deposits_depth": self.deposits_depth,
            "surface_friction": self.surface_friction,
            "snoclo": self.snoclo,
            "clrd": self.clrd,
        }
        d.update(super().as_dict())
        return d
