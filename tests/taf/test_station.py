from aeromet_py import Taf


def test_taf_station():
    code = """
    TAF SEQM 231655Z 2318/2418 35012KT 9999 SCT030 BKN100
        TEMPO 2320/2323 TS FEW023CB BKN026 BKN080
        BECMG 2400/2401 02005KT FEW008 BKN026 BKN080
        BECMG 2404/2406 VRB03KT 4000 BCFG BKN003 BKN020
        BECMG 2412/2414 9999 SCT023 SCT100 TX20/2319Z TN11/2411Z
    """
    taf = Taf(code)
    station = taf.station

    assert station.code == "SEQM"
    assert station.name == "QUITO/NEW INTL"
    assert station.icao == "SEQM"
    assert station.iata == "None"
    assert station.synop == "None"
    assert station.latitude == "00.07S"
    assert station.longitude == "078.21W"
    assert station.elevation == "2400"
    assert station.country == "Ecuador"
    assert (
        str(station)
        == "Name: QUITO/NEW INTL | Coordinates: 00.07S 078.21W | Elevation: 2400 m MSL | Country: Ecuador"
    )
