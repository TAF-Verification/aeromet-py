import re

from ...trend import Trend


class MetarTrend(Trend):
    """Basic structure for trend codes in METAR."""

    def __init__(self, match: re.Match) -> None:
        super().__init__(match)
