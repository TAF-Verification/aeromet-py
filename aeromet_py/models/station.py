from aeromet_py.database import get_country, get_stations

from .descriptor import DataDescriptor
from .group import Group


class Station(Group):
    """Basic structure for station code groups in reports from land stations."""

    _station = DataDescriptor()

    def __init__(self, code: str) -> None:
        self._station = [None for _ in range(8)]

        if code is not None:
            super().__init__(code)
            for stn in get_stations():
                if stn[1] == self._code or stn[2] == self._code or stn[3] == self._code:
                    self._station = stn
                    break

    def __str__(self) -> str:
        return (
            f"Name: {self.name} | "
            f"Coordinates: {self.latitude} {self.longitude} | "
            f"Elevation: {self.elevation} | "
            f"Country: {self.country}"
        )

    @property
    def name(self) -> str:
        """Returns the name of the station.

        Returns:
            str: the name.
        """
        return self._station[0]

    @property
    def icao(self) -> str:
        """Returns the ICAO code of the station.

        Returns:
            str: the ICAO code.
        """
        return self._station[1]

    @property
    def iata(self) -> str:
        """Returns the IATA code of the station.

        Returns:
            str: the IATA code.
        """
        return self._station[2]

    @property
    def synop(self) -> str:
        """Returns the SYNOP code of the station.

        Returns:
            str: the SYNOP code.
        """
        return self._station[3]

    @property
    def latitude(self) -> str:
        """Returns the latitude of the station.

        Returns:
            str: the latitude.
        """
        return self._station[4]

    @property
    def longitude(self) -> str:
        """Returns the longitude of the station.

        Returns:
            str: the longitude.
        """
        return self._station[5]

    @property
    def elevation(self) -> str:
        """Returns the elevation of the station.

        Returns:
            str: the elevation in meters over sea level.
        """
        return self._station[6]

    @property
    def country(self) -> str:
        """Returns the country where station is.

        Returns:
            str: the country.
        """
        return get_country(self._station[7])
