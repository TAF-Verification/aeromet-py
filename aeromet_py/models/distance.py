from ..utils import Conversions
from .numeric import Numeric


class Distance(Numeric):
    """Basic structure for distance attributes."""

    def __init__(self, code: str) -> None:
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

    def __str__(self) -> None:
        if self._value:
            return super().__str__() + " m"

        return super().__str__()

    @property
    def in_meters(self) -> float:
        """Get the distance in meters."""
        return self._value

    @property
    def in_kilometers(self) -> float:
        """Get the distance in kilometers."""
        return self.converted(Conversions.M_TO_KM)

    @property
    def in_sea_miles(self) -> float:
        """Get the distance in sea miles."""
        return self.converted(Conversions.M_TO_SMI)

    @property
    def in_feet(self) -> float:
        """Get the distance in feet."""
        return self.converted(Conversions.M_TO_FT)
