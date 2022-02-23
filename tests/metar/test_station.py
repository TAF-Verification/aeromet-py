from aeromet_py import Metar


def test_metar_station():
    metar = Metar(
        "METAR KJFK 122051Z 32004KT 10SM OVC065 M02/M15 A3031 RMK AO2 SLP264 T10171150 56004"
    )
    station = metar.station

    assert station.code == "KJFK"
    assert station.name == "NY NYC/JFK ARPT"
    assert station.icao == "KJFK"
    assert station.iata == "JFK"
    assert station.synop == "74486"
    assert station.latitude == "40.38N"
    assert station.longitude == "073.46W"
    assert station.elevation == "9"
    assert station.country == "United States of America (the)"
    assert (
        str(station)
        == "Name: NY NYC/JFK ARPT | Coordinates: 40.38N 073.46W | Elevation: 9 m MSL | Country: United States of America (the)"
    )
