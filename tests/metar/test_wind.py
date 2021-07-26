from aeromet_py import Metar

def test_wind_with_gust():
    metar = Metar("METAR SEQM 162000Z 34012G22KT 310V020 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018")
    wind = metar.wind
    
    assert wind.direction_in_degrees == 340.0
    assert wind.cardinal_direction == "NNW"
    assert wind.direction_in_radians == 5.934119456780721
    assert wind.speed_in_knot == 12.0
    assert wind.speed_in_kph == 22.224
    assert wind.gust_in_knot == 22.0
    assert wind.gust_in_mps == 11.31777768
    assert wind.gust_in_miph == 25.317159999999998

def test_wind_without_gust():
    metar = Metar("METAR SEQM 162000Z 34012KT 310V020 9999 VCSH SCT030 BKN200 21/12 Q1022 NOSIG RMK A3018")
    wind = metar.wind
    
    assert wind.direction_in_degrees == 340.0
    assert wind.cardinal_direction == "NNW"
    assert wind.direction_in_radians == 5.934119456780721
    assert wind.speed_in_knot == 12.0
    assert wind.speed_in_kph == 22.224
    assert wind.gust_in_knot == None
    assert wind.gust_in_mps == None
    assert wind.gust_in_miph == None
    