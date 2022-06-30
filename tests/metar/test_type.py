from aeromet_py import Metar


def test_metar_type():
    metar = Metar("METAR UUDD 060000Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type_.code == "METAR"
    assert metar.type_.type == "Meteorological Aerodrome Report"
    assert str(metar.type_) == "Meteorological Aerodrome Report (METAR)"
    assert metar.type_.as_dict() == {
        "code": "METAR",
        "type": "Meteorological Aerodrome Report",
    }


def test_special_type():
    metar = Metar("SPECI UUDD 060030Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type_.code == "SPECI"
    assert metar.type_.type == "Special Aerodrome Report"
    assert str(metar.type_) == "Special Aerodrome Report (SPECI)"
    assert metar.type_.as_dict() == {
        "code": "SPECI",
        "type": "Special Aerodrome Report",
    }


def test_no_type():
    metar = Metar("UUDD 060030Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type_.code == "METAR"
    assert metar.type_.type == "Meteorological Aerodrome Report"
    assert str(metar.type_) == "Meteorological Aerodrome Report (METAR)"
    assert metar.type_.as_dict() == {
        "code": "METAR",
        "type": "Meteorological Aerodrome Report",
    }
