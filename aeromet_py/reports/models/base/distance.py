from typing import Any, Dict, Optional

from ....utils import Conversions
from .numeric import Numeric


class Distance(Numeric):
    """Basic structure for distance attributes."""

    def __init__(self, code: Optional[str]) -> None:
        if code is None:
            code = "////"

        if code == "9999":
            code = "10000"

        try:
            _distance = float(code)
        except ValueError:
            _distance = None
        finally:
            super().__init__(_distance)

    def __str__(self) -> str:
        if self._value:
            return super().__str__() + " m"

        return super().__str__()

    @property
    def in_meters(self) -> Optional[float]:
        """Get the distance in meters."""
        return self._value

    @property
    def in_kilometers(self) -> Optional[float]:
        """Get the distance in kilometers."""
        return self.converted(factor=Conversions.M_TO_KM)

    @property
    def in_sea_miles(self) -> Optional[float]:
        """Get the distance in sea miles."""
        return self.converted(factor=Conversions.M_TO_SMI)

    @property
    def in_feet(self) -> Optional[float]:
        """Get the distance in feet."""
        return self.converted(factor=Conversions.M_TO_FT)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "units": "meters",
            "distance": self.in_meters,
        }
