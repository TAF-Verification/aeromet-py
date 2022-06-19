import pytest

from aeromet_py import Metar


def test_one_windshear():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07 NOSIG"
    )
    windshear = metar.windshear

    assert windshear.codes == ["WS R07"]
    assert str(windshear) == "07"
    assert windshear.all_runways == False
    assert windshear[0].code == "WS R07"
    assert windshear[0].name == "07"
    assert windshear[0].all == False

    with pytest.raises(IndexError):
        assert windshear[1].code == None


def test_two_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07L WS R25C NOSIG"
    )
    windshear = metar.windshear

    assert windshear.codes == ["WS R07L", "WS R25C"]
    assert str(windshear) == "07 left | 25 center"
    assert windshear.all_runways == False
    assert windshear[0].code == "WS R07L"
    assert windshear[0].name == "07 left"
    assert windshear[0].all == False
    assert windshear[1].code == "WS R25C"
    assert windshear[1].name == "25 center"
    assert windshear[1].all == False

    with pytest.raises(IndexError):
        assert windshear[2].code == None


def test_all_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS ALL RWY NOSIG"
    )
    windshear = metar.windshear

    assert windshear.codes == ["WS ALL RWY"]
    assert str(windshear) == "all runways"
    assert windshear.all_runways == True
    assert windshear[0].code == "WS ALL RWY"
    assert windshear[0].name == None
    assert windshear[0].all == True

    with pytest.raises(IndexError):
        assert windshear[1].code == None


def test_no_windshears():
    metar = Metar(
        "LTAD 212106Z 25004KT 9999 SCT040 BKN100 16/14 Q1019 RESHRA NOSIG RMK RWY29 VRB02KT"
    )
    windshear = metar.windshear

    assert windshear.codes == []
    assert str(windshear) == ""
    assert windshear.all_runways == False

    for i in range(3):
        with pytest.raises(IndexError):
            assert windshear[i].code == None
