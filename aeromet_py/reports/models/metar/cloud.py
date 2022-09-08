import re

from ..base import Cloud, CloudList, HasConcatenateStringProntocol


class MetarCloudMixin(HasConcatenateStringProntocol):
    """Mixin to add clouds attribute to the report."""

    def __init__(self) -> None:
        self._clouds = CloudList()

    def _handle_cloud(self, match: re.Match) -> None:
        cloud: Cloud = Cloud.from_metar(match)
        self._clouds.add(cloud)

        self._concatenate_string(cloud)

    @property
    def clouds(self) -> CloudList:
        """Get the cloud groups data of the METAR."""
        return self._clouds
