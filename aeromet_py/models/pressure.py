from ..utils import Conversions
from .numeric import Numeric


class Pressure(Numeric):
    """Basic structure for pressure attributes."""

    def __init__(self, code: str) -> None:
        if code is None:
            code = "////"

        try:
            _pressure = float(code)
        except ValueError:
            _pressure = None
        finally:
            super().__init__(_pressure)

    def __str__(self) -> str:
        if self._value:
            return super().__str__() + " hPa"

        return super().__str__()

    @property
    def in_hPa(self) -> float:
        """Get the pressure in hecto pascals (hPa)."""
        return self._value

    @property
    def in_inHg(self) -> float:
        """Get the pressure in mercury inches (inHg)."""
        return self.converted(Conversions.HPA_TO_INHG)

    @property
    def in_mbar(self) -> float:
        """Get the pressure in millibars (mbar)."""
        return self.converted(Conversions.HPA_TO_MBAR)

    @property
    def in_bar(self) -> float:
        """Get the pressure in bars (bar)."""
        return self.converted(Conversions.HPA_TO_BAR)

    @property
    def in_atm(self) -> float:
        """Get the pressure in atmospheres (atm)."""
        return self.converted(Conversions.HPA_TO_ATM)