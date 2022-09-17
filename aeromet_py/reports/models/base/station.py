from typing import Dict, List, Optional

from ....database import get_country, get_stations
from .group import Group


CODE_TYPES: Dict[str, int] = {
    "ICAO": 1,
    "IATA": 2,
    "SYNOP": 3,
}


class Station(Group):
    """Basic structure for station code groups in reports from land stations.

    Args:
        code (str): the land station code from the report (MROC, SJO, 78762).
        type (str): the type of land station code (ICAO, IATA, SYNOP).
    """

    def __init__(self, code: str, type: str) -> None:
        super().__init__(code)

        if code is not None:
            self._station = self._get_data(code, CODE_TYPES.get(type))
        else:
            self._station = [None for _ in range(8)]

    def _get_data(self, code: str, index: int) -> List[Optional[str]]:
        for stn in get_stations():
            if code == stn[index]:
                return stn

        return [None for _ in range(8)]

    def __str__(self) -> str:
        return (
            f"Name: {self.name} | "
            f"Coordinates: {self.latitude} {self.longitude} | "
            f"Elevation: {self.elevation} m MSL | "
            f"Country: {self.country}"
        )

    @property
    def name(self) -> Optional[str]:
        """Get the name of the station."""
        return self._station[0]

    @property
    def icao(self) -> Optional[str]:
        """Get the ICAO code of the station."""
        return self._station[1]

    @property
    def iata(self) -> Optional[str]:
        """Get the IATA code of the stations."""
        return self._station[2]

    @property
    def synop(self) -> Optional[str]:
        """Get the SYNOP code of the station."""
        return self._station[3]

    @property
    def latitude(self) -> Optional[str]:
        """Get the latitude of the station."""
        return self._station[4]

    @property
    def longitude(self) -> Optional[str]:
        """Get the longitude of the station."""
        return self._station[5]

    @property
    def elevation(self) -> Optional[str]:
        """Get the elevation in meters above sea level of the station."""
        return self._station[6]

    @property
    def country(self) -> Optional[str]:
        """The country to which the land station belongs."""
        return get_country(self._station[7])

    def as_dict(self) -> Dict[str, Optional[str]]:
        d = {
            "name": self.name,
            "icao": self.icao,
            "iata": self.iata,
            "synop": self.synop,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation": self.elevation,
            "country": self.country,
        }
        d.update(super().as_dict())
        return d
