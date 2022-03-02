from pytest import approx, raises

from aeromet_py import Taf

_year: int = 2020
_month: int = 5


def test_temperatures_in_taf():
    code = """
    TAF AMD RKNY 021725Z 0218/0324 26017G35KT CAVOK TX07/0305Z TNM03/0321Z
        BECMG 0223/0224 27010KT
        BECMG 0302/0303 03006KT
        BECMG 0308/0309 23006KT
    """
    taf = Taf(code, year=_year, month=_month)
    max_temp = taf.max_temperature
    min_temp = taf.min_temperature

    assert max_temp.code == "TX07/0305Z"
    assert str(max_temp) == "7.0°C at 2020-05-03 05:00:00"
    assert max_temp.in_celsius == 7.0
    assert max_temp.in_kelvin == 280.15
    assert max_temp.in_fahrenheit == 44.6
    assert max_temp.in_rankine == approx(504.27)

    assert min_temp.code == "TNM03/0321Z"
    assert str(min_temp) == "-3.0°C at 2020-05-03 21:00:00"
    assert min_temp.in_celsius == -3.0
    assert min_temp.in_kelvin == 270.15
    assert min_temp.in_fahrenheit == 26.6
    assert min_temp.in_rankine == approx(486.27)

    assert max_temp.time.year == 2020


def test_no_temperatures_in_taf():
    code = """
    TAF RPMD 021700Z 0218/0318 36006KT 9999 FEW016 SCT090
        TEMPO 0306/0312 13008KT -SHRA FEW014CB SCT015 BKN090
    """
    taf = Taf(code, year=_year, month=_month)
    max_temp = taf.max_temperature
    min_temp = taf.min_temperature

    assert max_temp.code == None
    assert str(max_temp) == ""
    assert max_temp.in_celsius == None
    assert max_temp.in_kelvin == None
    assert max_temp.in_fahrenheit == None
    assert max_temp.in_rankine == None

    assert min_temp.code == None
    assert str(min_temp) == ""
    assert min_temp.in_celsius == None
    assert min_temp.in_kelvin == None
    assert min_temp.in_fahrenheit == None
    assert min_temp.in_rankine == None

    with raises(AttributeError):
        assert max_temp.time.year == 2020
