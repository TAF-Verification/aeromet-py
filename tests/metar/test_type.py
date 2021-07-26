from aeromet_py import Metar
import pytest

def test_metar_type():
    metar = Metar('METAR UUDD 060000Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG')
    assert metar.type.type == "Meteorological Aerodrome Report"


def test_special_type():
    metar = Metar('SPECI UUDD 060030Z 18004MPS CAVOK M01/M04 Q1002 R14R/CLRD60 NOSIG')
    assert metar.type.type == "Special Aerodrome Report"