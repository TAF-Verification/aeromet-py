from .numeric import Numeric


class Distance(Numeric):
    """Basic structure for distance attributes."""

    def __init__(self, code: str) -> None:
        if code is None:
            code = "////"

        if code == "9999":
            code = "10000"

        try:
            _visibility = float(code)
        except ValueError:
            _visibility = None
        finally:
            super().__init__(_visibility)

    def __str__(self) -> None:
        if self._value:
            return super().__str__() + " m"

        return super().__str__()
