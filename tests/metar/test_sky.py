from aeromet_py import Metar

def test_two_layers():
    metar = Metar("METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016")
    sky = metar.sky
    
    assert sky.codes == ("FEW049", "BKN056")
    assert sky.first.code == "FEW049"
    assert sky.first.height_in_feet == 4900.0
    assert sky.first.cloud == None
    assert sky.first.height_in_meters == 1493.52
    assert sky.second.code == "BKN056"
    assert sky.second.height_in_feet == 5600.0
    assert sky.second.cloud == None
    assert sky.second.height_in_meters == 1706.88


def test_three_layers():
    metar = Metar("METAR KMIA 191458Z 33006KT 5SM R09/1800V4500FT -TSRA BR FEW013 BKN021CB OVC040 23/21 A3003 RMK AO2 OCNL LTGICCG OHD TS OHD MOV SE P0007 T02280211")
    sky = metar.sky
    
    assert sky.codes == ("FEW013", "BKN021CB", "OVC040")
    assert sky.first.code == "FEW013"
    assert sky.first.height_in_feet == 1300.0
    assert sky.first.cloud == None
    assert sky.first.height_in_meters == 396.24
    assert sky.second.code == "BKN021CB"
    assert sky.second.height_in_feet == 2100.0
    assert sky.second.cloud == "cumulonimbus"
    assert sky.second.height_in_meters == 640.08
    assert sky.third.code == "OVC040"
    assert sky.third.height_in_feet == 4000.0
    assert sky.third.cloud == None
    assert sky.third.height_in_meters == 1219.2