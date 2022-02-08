from aeromet_py import Metar


def test_trend_wind_with_gust():
    metar = Metar(
        "METAR SEQM 050400Z 04010KT 9999 BKN006 OVC030 14/12 Q1028 BECMG 09012G22KT RMK A3037"
    )
    wind = metar.trend_wind

    assert wind.code == "09012G22KT"
    assert wind.cardinal_direction == "E"
    assert wind.direction_in_degrees == 90.0
    assert wind.direction_in_radians == 1.5707963267948966
    assert wind.variable == False
    assert wind.speed_in_knot == 12.0
    assert wind.speed_in_mps == 6.17333328
    assert wind.speed_in_kph == 22.224
    assert wind.gust_in_knot == 22.0
    assert wind.gust_in_mps == 11.31777768
    assert wind.gust_in_miph == 25.317159999999998
    assert str(wind) == "E (90.0°) 12.0 kt gusts of 22.0 kt"


def test_trend_wind_without_gust():
    metar = Metar("METAR LPPT 082000Z 29003KT CAVOK 14/07 Q1026 BECMG 34012KT")
    wind = metar.trend_wind

    assert wind.code == "34012KT"
    assert wind.cardinal_direction == "NNW"
    assert wind.direction_in_degrees == 340.0
    assert wind.direction_in_radians == 5.934119456780721
    assert wind.variable == False
    assert wind.speed_in_knot == 12.0
    assert wind.speed_in_mps == 6.17333328
    assert wind.speed_in_kph == 22.224
    assert wind.gust_in_knot == None
    assert wind.gust_in_mps == None
    assert wind.gust_in_miph == None
    assert str(wind) == "NNW (340.0°) 12.0 kt"


def test_no_wind():
    metar = Metar(
        "METAR SEQM 162000Z 08005KT 9999 VCSH SCT030 BKN200 21/12 Q1022 TEMPO RA RMK A3018"
    )
    wind = metar.trend_wind

    assert wind.code == None
    assert wind.direction_in_degrees == None
    assert wind.cardinal_direction == None
    assert wind.direction_in_radians == None
    assert wind.variable == False
    assert wind.speed_in_knot == None
    assert wind.speed_in_mps == None
    assert wind.speed_in_kph == None
    assert wind.gust_in_knot == None
    assert wind.gust_in_mps == None
    assert wind.gust_in_miph == None
    assert str(wind) == ""
