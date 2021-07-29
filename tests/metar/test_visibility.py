from aeromet_py import Metar

def test_visibility_4digits():
    metar = Metar("METAR SBBV 170400Z 08004KT 9999 SCT030 FEW035TCU BKN070 26/23 Q1012")
    
    assert metar.visibility.in_meters == 10_000.0
    assert metar.visibility.in_kilometers == 10.0
    assert metar.visibility.in_sea_miles == 5.399568034557235
    assert metar.visibility.cavok == False


def test_visibility_in_seamiles():
    metar = Metar("METAR PALH 170933Z 00000KT 1 1/4SM BR FEW002 M14/M16 A2980 RMK AO2 T11441156")
    
    assert metar.visibility.in_meters == 2315.0
    assert metar.visibility.in_kilometers == 2.315
    assert metar.visibility.in_sea_miles == 1.2499999999999998
    assert metar.visibility.cavok == False


def test_minimum_visibility():
    metar = Metar("METAR UUDD 180100Z 00000MPS 4800 2100NW -SN BR SCT025 M02/M03 Q1007 R32L/290042 NOSIG")
    
    assert metar.minimum_visibility.in_meters == 2100.0
    assert metar.minimum_visibility.in_kilometers == 2.1
    assert metar.minimum_visibility.in_sea_miles == 1.1339092872570193
    assert metar.minimum_visibility.cardinal_direction == "NW"
    assert metar.minimum_visibility.direction_in_degrees == 315.0