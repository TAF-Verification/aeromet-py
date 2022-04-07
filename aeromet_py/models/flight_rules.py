from typing import Dict, List

FLIGHT_RULES: Dict[str, List[float]] = {
    "VLIFR": [60.0, 800.0],
    "LIFR": [150.0, 1600.0],
    "IFR": [300.0, 5000.0],
    "MVFR": [900.0, 8000.0],
    "VFR": [40000.0, 20000.0],
}


class FlightRulesMixin:
    """
    Mixin to add flight rules to the report or forecast.
    The class must have MetarPrevailingMixin and MetarCloudMixin
    implemented.
    """

    @property
    def flight_rules(self) -> str:
        """Get the flight rules of the report or forecast."""
        prevailing: float = self._prevailing.in_meters
        ceiling: float = None
        if len(self._clouds) > 0:
            for cloud in self._clouds.items:
                if cloud.cover in ["broken", "overcast", "indefinite ceiling"]:
                    ceiling = cloud.height_in_meters
                    break

        if prevailing is None and ceiling is None:
            return None

        rules: List[float]
        for flight_rule, rules in FLIGHT_RULES.items():
            if prevailing is not None and ceiling is not None:
                if ceiling < rules[0] or prevailing < rules[1]:
                    return flight_rule
            elif prevailing is not None and ceiling is None:
                if prevailing < rules[1]:
                    return flight_rule
            elif prevailing is None and ceiling is not None:
                if ceiling < rules[0]:
                    return flight_rule
            else:
                return "VFR"
