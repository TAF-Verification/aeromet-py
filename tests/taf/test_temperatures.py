from pytest import approx, raises

from aeromet_py import Taf

_year: int = 2020
_month: int = 5


def test_one_max_one_min_temperature_in_taf():
    code = """
    TAF AMD RKNY 021725Z 0218/0324 26017G35KT CAVOK TX07/0305Z TNM03/0321Z
        BECMG 0223/0224 27010KT
        BECMG 0302/0303 03006KT
        BECMG 0308/0309 23006KT
    """
    taf = Taf(code, year=_year, month=_month)
    max_temps = taf.max_temperatures

    assert max_temps.codes == ["TX07/0305Z"]
    assert str(max_temps) == "7.0°C at 2020-05-03 05:00:00"
    assert max_temps.as_dict() == {
        "first": {
            "code": None,
            "datetime": "2020-05-03 05:00:00",
            "temperature": 7.0,
            "units": "celsius",
        }
    }

    first_max = max_temps[0]
    assert first_max.code == "TX07/0305Z"
    assert str(first_max) == "7.0°C at 2020-05-03 05:00:00"
    assert first_max.in_celsius == 7.0
    assert first_max.in_kelvin == 280.15
    assert first_max.in_fahrenheit == 44.6
    assert first_max.in_rankine == approx(504.27)

    assert first_max.time.year == 2020

    with raises(IndexError):
        assert max_temps[1].code == None

    min_temps = taf.min_temperatures

    assert min_temps.codes == ["TNM03/0321Z"]
    assert str(min_temps) == "-3.0°C at 2020-05-03 21:00:00"
    assert min_temps.as_dict() == {
        "first": {
            "code": None,
            "datetime": "2020-05-03 21:00:00",
            "temperature": -3.0,
            "units": "celsius",
        }
    }

    first_min = min_temps[0]
    assert first_min.code == "TNM03/0321Z"
    assert str(first_min) == "-3.0°C at 2020-05-03 21:00:00"
    assert first_min.in_celsius == -3.0
    assert first_min.in_kelvin == 270.15
    assert first_min.in_fahrenheit == 26.6
    assert first_min.in_rankine == approx(486.27)

    assert first_min.time.year == 2020

    with raises(IndexError):
        assert min_temps[1].code == None


def test_two_max_temperatures_in_taf():
    code = "TAF DXNG 301700Z 3018/3118 VRB03KT 9999 FEW010 TX30/3019Z TN20/3110Z TX28/3117Z"
    taf = Taf(code, year=_year, month=_month)
    max_temps = taf.max_temperatures

    assert max_temps.codes == ["TX30/3019Z", "TX28/3117Z"]
    assert (
        str(max_temps)
        == "30.0°C at 2020-05-30 19:00:00 | 28.0°C at 2020-05-31 17:00:00"
    )
    assert max_temps.as_dict() == {
        "first": {
            "code": None,
            "datetime": "2020-05-30 19:00:00",
            "temperature": 30.0,
            "units": "celsius",
        },
        "second": {
            "code": None,
            "datetime": "2020-05-31 17:00:00",
            "temperature": 28.0,
            "units": "celsius",
        },
    }

    first_max = max_temps[0]
    assert first_max.code == "TX30/3019Z"
    assert str(first_max) == "30.0°C at 2020-05-30 19:00:00"
    assert first_max.in_celsius == 30.0
    assert first_max.in_kelvin == 303.15
    assert first_max.in_fahrenheit == 86.0
    assert first_max.in_rankine == approx(545.67)

    second_max = max_temps[1]
    assert second_max.code == "TX28/3117Z"
    assert str(second_max) == "28.0°C at 2020-05-31 17:00:00"
    assert second_max.in_celsius == 28.0
    assert second_max.in_kelvin == 301.15
    assert second_max.in_fahrenheit == 82.4
    assert second_max.in_rankine == 542.07


def test_no_temperatures_in_taf():
    code = """
    TAF RPMD 021700Z 0218/0318 36006KT 9999 FEW016 SCT090
        TEMPO 0306/0312 13008KT -SHRA FEW014CB SCT015 BKN090
    """
    taf = Taf(code, year=_year, month=_month)

    max_temps = taf.max_temperatures
    assert max_temps.as_dict() == {}

    min_temps = taf.min_temperatures
    assert min_temps.as_dict() == {}

    with raises(IndexError):
        assert max_temps[0].time.year == 2020

    with raises(IndexError):
        assert min_temps[0].time.year == 2020
