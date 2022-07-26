from typing import Any, Dict, Optional

from ....utils import Conversions
from .numeric import Numeric


class Pressure(Numeric):
    """Basic structure for pressure attributes."""

    def __init__(self, code: Optional[str]) -> None:
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
    def in_hPa(self) -> Optional[float]:
        """Get the pressure in hecto pascals (hPa)."""
        return self._value

    @property
    def in_inHg(self) -> Optional[float]:
        """Get the pressure in mercury inches (inHg)."""
        return self.converted(factor=Conversions.HPA_TO_INHG)

    @property
    def in_mbar(self) -> Optional[float]:
        """Get the pressure in millibars (mbar)."""
        return self.converted(factor=Conversions.HPA_TO_MBAR)

    @property
    def in_bar(self) -> Optional[float]:
        """Get the pressure in bars (bar)."""
        return self.converted(factor=Conversions.HPA_TO_BAR)

    @property
    def in_atm(self) -> Optional[float]:
        """Get the pressure in atmospheres (atm)."""
        return self.converted(factor=Conversions.HPA_TO_ATM)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "units": "hectopascals",
            "pressure": self.in_hPa,
        }
