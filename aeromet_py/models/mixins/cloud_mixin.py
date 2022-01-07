import re

from ..cloud import CloudLayer, CloudList


class CloudMixin:
    """Mixin to add cloud list attribute to the report."""

    def __init__(self) -> None:
        self._clouds = CloudList()

    def _handle_cloud(self, match: re.Match) -> None:
        _cloud: CloudLayer = CloudLayer(match)
        self._clouds.add(_cloud)

        self._concatenate_string(_cloud)

    @property
    def clouds(self) -> CloudList:
        """Returns the cloud data of the report.

        Returns:
            CloudList: the list of CloudLayer class instance.
        """
        return self._clouds
