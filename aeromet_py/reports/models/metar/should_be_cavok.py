from typing_extensions import Protocol

from ..base import GroupList
from .cloud import CloudList
from .visibility import MetarPrevailingVisibility
from .weather import MetarWeather


class HasPrevailingCloudsWeatherProtocol(Protocol):
    @property
    def prevailing_visibility(self) -> MetarPrevailingVisibility:
        pass

    @property
    def weathers(self) -> GroupList[MetarWeather]:
        pass

    @property
    def clouds(self) -> CloudList:
        pass


class ShouldBeCavokMixin(HasPrevailingCloudsWeatherProtocol):
    """Mixin to add _verify_cavok method to the report."""

    def should_be_cavok(self) -> bool:
        """Analyses the conditions for CAVOK in the report. Returns `True` if CAVOK should
        be reported, `False` if not or if there is no data to make a complete analysis."""
        if len(self.weathers) > 0:
            return False

        if self.clouds.ceiling:
            return False

        if self.prevailing_visibility.in_meters is None or len(self.clouds) == 0:
            return False

        if (
            self.prevailing_visibility.in_meters is not None
            and self.prevailing_visibility.in_meters < 10_000.0
        ):
            return False

        for c in self.clouds:
            if c.cover is "indefinite ceiling":
                return False

            if c.cloud_type == "cumulonimbus" or c.cloud_type == "towering cumulus":
                return False

            if c.height_in_feet is not None and c.height_in_feet < 4999.99999999:
                return False

        return True
