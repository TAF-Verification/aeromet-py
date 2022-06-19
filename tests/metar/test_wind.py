from aeromet_py import Metar


def test_wind_with_gust():
    metar = Metar(
        "METAR SEQM 162000Z 09012G22KT 310V020 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018"
    )
    wind = metar.wind

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
    assert str(wind) == "E (90.0°) 12.0 kt gust of 22.0 kt"


def test_wind_without_gust():
    metar = Metar(
        "METAR SEQM 162000Z 34012KT 310V020 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018"
    )
    wind = metar.wind

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


def test_variable_wind():
    metar = Metar(
        "METAR SEQM 162000Z VRB02KT 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018"
    )
    wind = metar.wind

    assert wind.code == "VRB02KT"
    assert wind.cardinal_direction == None
    assert wind.direction_in_degrees == None
    assert wind.direction_in_radians == None
    assert wind.variable == True
    assert wind.speed_in_knot == 2
    assert wind.speed_in_mps == 1.02888888
    assert wind.speed_in_kph == 3.704
    assert wind.gust_in_knot == None
    assert wind.gust_in_mps == None
    assert wind.gust_in_miph == None
    assert str(wind) == "variable wind 2.0 kt"


def test_no_wind():
    metar = Metar(
        "METAR SEQM 162000Z /////KT 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018"
    )
    wind = metar.wind

    assert wind.code == "/////KT"
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


def test_wind_variation():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 310V020 8000 RA BR VCTS SCT008CB OVC020 04/03 Q1013"
    )
    wind_variation = metar.wind_variation

    assert wind_variation.from_cardinal_direction == "NW"
    assert wind_variation.from_in_degrees == 310.0
    assert wind_variation.from_in_radians == 5.410520681182422
    assert wind_variation.to_cardinal_direction == "NNE"
    assert wind_variation.to_in_degrees == 20.0
    assert wind_variation.to_in_radians == 0.3490658503988659
    assert str(wind_variation) == "from NW (310.0°) to NNE (20.0°)"


def test_no_wind_variation():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 8000 RA BR VCTS SCT008CB OVC020 04/03 Q1013"
    )
    wind_variation = metar.wind_variation

    assert wind_variation.from_cardinal_direction == None
    assert wind_variation.from_in_degrees == None
    assert wind_variation.from_in_radians == None
    assert wind_variation.to_cardinal_direction == None
    assert wind_variation.to_in_degrees == None
    assert wind_variation.to_in_radians == None
    assert str(wind_variation) == ""
