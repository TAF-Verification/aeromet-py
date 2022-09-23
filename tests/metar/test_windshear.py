import pytest

from aeromet_py import Metar


def test_one_windshear():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07 NOSIG"
    )
    windshears = metar.windshears

    assert windshears.codes == ["WS R07"]
    assert str(windshears) == "07"
    assert windshears.all_runways == False
    assert windshears[0].code == "WS R07"
    assert windshears[0].name == "07"
    assert windshears[0].all_ == False
    assert windshears[0].as_dict() == {
        "all": False,
        "code": "WS R07",
        "name": "07",
    }

    with pytest.raises(IndexError):
        assert windshears[1].code == None


def test_two_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07L WS R25C NOSIG"
    )
    windshears = metar.windshears

    assert windshears.codes == ["WS R07L", "WS R25C"]
    assert str(windshears) == "07 left | 25 center"
    assert windshears.all_runways == False
    assert windshears[0].code == "WS R07L"
    assert windshears[0].name == "07 left"
    assert windshears[0].all_ == False
    assert windshears[0].as_dict() == {
        "all": False,
        "code": "WS R07L",
        "name": "07 left",
    }

    assert windshears[1].code == "WS R25C"
    assert windshears[1].name == "25 center"
    assert windshears[1].all_ == False
    assert windshears[1].as_dict() == {
        "all": False,
        "code": "WS R25C",
        "name": "25 center",
    }

    with pytest.raises(IndexError):
        assert windshears[2].code == None


def test_all_windshears():
    metar = Metar(
        "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS ALL RWY NOSIG"
    )
    windshears = metar.windshears

    assert windshears.codes == ["WS ALL RWY"]
    assert str(windshears) == "all runways"
    assert windshears.all_runways == True
    assert windshears[0].code == "WS ALL RWY"
    assert windshears[0].name == None
    assert windshears[0].all_ == True
    assert windshears[0].as_dict() == {"all": True, "code": "WS ALL RWY", "name": None}

    with pytest.raises(IndexError):
        assert windshears[1].code == None


def test_no_windshears():
    metar = Metar(
        "LTAD 212106Z 25004KT 9999 SCT040 BKN100 16/14 Q1019 RESHRA NOSIG RMK RWY29 VRB02KT"
    )
    windshears = metar.windshears

    assert windshears.codes == []
    assert str(windshears) == ""
    assert windshears.all_runways == False
    assert windshears.as_dict() == {}

    for i in range(3):
        with pytest.raises(IndexError):
            assert windshears[i].code == None
