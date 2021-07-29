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


def test_no_visibility():
    metar = Metar("METAR PALH 170933Z 00000KT BR FEW002 M14/M16 A2980 RMK AO2 T11441156")
    
    assert metar.visibility.in_meters == None
    assert metar.visibility.in_kilometers == None
    assert metar.visibility.in_sea_miles == None
    assert metar.visibility.cavok == False


def test_minimum_visibility():
    metar = Metar("METAR UUDD 180100Z 00000MPS 4800 2100NW -SN BR SCT025 M02/M03 Q1007 R32L/290042 NOSIG")
    min_vis = metar.minimum_visibility
    
    assert min_vis.direction_in_degrees == 315.0
    assert min_vis.cardinal_direction == "NW"
    assert min_vis.direction_in_radians == 5.497787143782138
    assert min_vis.in_kilometers == 2.1
    assert min_vis.in_meters == 2100.0
    assert min_vis.in_sea_miles == 1.1339092872570193


def test_no_minimum_visibility():
    metar = Metar("METAR UUDD 180100Z 25005MPS 4800 -SN BR SCT025 M02/M03 Q1007 R32L/290042 NOSIG")
    min_vis = metar.minimum_visibility
    
    assert min_vis.direction_in_degrees == None
    assert min_vis.cardinal_direction == None
    assert min_vis.direction_in_radians == None
    assert min_vis.in_kilometers == None
    assert min_vis.in_meters == None
    assert min_vis.in_sea_miles == None