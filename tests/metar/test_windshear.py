from aeromet_py import Metar


def test_one_windshear():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07 NOSIG"
    )
    windshear = metar.windshear

    assert windshear.first.runway_name == "07"
    assert windshear.second.runway_name == None
    assert windshear.thrid.runway_name == None
    assert windshear.all_runways == False
    assert str(windshear) == "07"


def test_two_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07L WS R25C NOSIG"
    )
    windshear = metar.windshear

    assert windshear.first.runway_name == "07 left"
    assert windshear.second.runway_name == "25 center"
    assert windshear.thrid.runway_name == None
    assert windshear.all_runways == False
    assert str(windshear) == "07 left | 25 center"


def test_all_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS ALL RWY NOSIG"
    )
    windshear = metar.windshear

    assert windshear.first.runway_name == None
    assert windshear.second.runway_name == None
    assert windshear.thrid.runway_name == None
    assert windshear.all_runways == True
    assert str(windshear) == "all runways"


def test_no_windshears():
    metar = Metar(
        "LTAD 212106Z 25004KT 9999 SCT040 BKN100 16/14 Q1019 RESHRA NOSIG RMK RWY29 VRB02KT"
    )
    windshear = metar.windshear

    assert windshear.first.runway_name == None
    assert windshear.second.runway_name == None
    assert windshear.thrid.runway_name == None
    assert windshear.all_runways == False
    assert str(windshear) == ""
