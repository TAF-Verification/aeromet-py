from aeromet_py import Metar


def test_metar_type():
    metar = Metar("METAR UUDD 060000Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type.code == "METAR"
    assert metar.type.type == "Meteorological Aerodrome Report"
    assert str(metar.type) == "Meteorological Aerodrome Report (METAR)"


def test_special_type():
    metar = Metar("SPECI UUDD 060030Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type.code == "SPECI"
    assert metar.type.type == "Special Aerodrome Report"
    assert str(metar.type) == "Special Aerodrome Report (SPECI)"


def test_no_type():
    metar = Metar("UUDD 060030Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG")
    assert metar.type.code == "METAR"
    assert metar.type.type == "Meteorological Aerodrome Report"
    assert str(metar.type) == "Meteorological Aerodrome Report (METAR)"
