import pytest

from aeromet_py import Metar

_year: int = 2021
_month: int = 5


def test_weather_trend_wind_with_gust():
    metar = Metar(
        "METAR SEQM 050400Z 04010KT 9999 BKN006 OVC030 14/12 Q1028 TEMPO 09012G22KT RMK A3037",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO 09012G22KT"]
    assert (
        str(trends) == "temporary from 2021-05-05 04:00:00 until 2021-05-05 06:00:00\n"
        "E (90.0°) 12.0 kt gust of 22.0 kt"
    )

    first = trends[0]
    assert first.code == "TEMPO 09012G22KT"
    assert first.wind.code == "09012G22KT"
    assert first.wind.cardinal_direction == "E"
    assert first.wind.direction_in_degrees == 90.0
    assert first.wind.direction_in_radians == 1.5707963267948966
    assert first.wind.variable == False
    assert first.wind.speed_in_knot == 12.0
    assert first.wind.speed_in_mps == 6.17333328
    assert first.wind.speed_in_kph == 22.224
    assert first.wind.gust_in_knot == 22.0
    assert first.wind.gust_in_mps == 11.31777768
    assert first.wind.gust_in_miph == 25.317159999999998
    assert first.wind.as_dict() == {
        "code": "09012G22KT",
        "direction": {
            "cardinal": "E",
            "direction": 90.0,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": 22.0, "units": "knot"},
        "speed": {"speed": 12.0, "units": "knot"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_wind_without_gust():
    metar = Metar(
        "METAR LPPT 082000Z 29003KT CAVOK 14/07 Q1026 BECMG 34012KT",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG 34012KT"]
    assert (
        str(trends) == "becoming from 2021-05-08 20:00:00 until 2021-05-08 22:00:00\n"
        "NNW (340.0°) 12.0 kt"
    )

    first = trends[0]
    assert first.code == "BECMG 34012KT"
    assert first.wind.code == "34012KT"
    assert first.wind.cardinal_direction == "NNW"
    assert first.wind.direction_in_degrees == 340.0
    assert first.wind.direction_in_radians == 5.934119456780721
    assert first.wind.variable == False
    assert first.wind.speed_in_knot == 12.0
    assert first.wind.speed_in_mps == 6.17333328
    assert first.wind.speed_in_kph == 22.224
    assert first.wind.gust_in_knot == None
    assert first.wind.gust_in_mps == None
    assert first.wind.gust_in_miph == None
    assert first.wind.as_dict() == {
        "code": "34012KT",
        "direction": {
            "cardinal": "NNW",
            "direction": 340.0,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": None, "units": "knot"},
        "speed": {"speed": 12.0, "units": "knot"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_no_wind():
    metar = Metar(
        "METAR SEQM 162000Z 08005KT 9999 VCSH SCT030 BKN200 21/12 Q1022 TEMPO RA RMK A3018",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO RA"]
    assert (
        str(trends) == "temporary from 2021-05-16 20:00:00 until 2021-05-16 22:00:00\n"
        "rain"
    )

    first = trends[0]
    assert first.code == "TEMPO RA"
    assert first.wind.code == None
    assert first.wind.direction_in_degrees == None
    assert first.wind.cardinal_direction == None
    assert first.wind.direction_in_radians == None
    assert first.wind.variable == False
    assert first.wind.speed_in_knot == None
    assert first.wind.speed_in_mps == None
    assert first.wind.speed_in_kph == None
    assert first.wind.gust_in_knot == None
    assert first.wind.gust_in_mps == None
    assert first.wind.gust_in_miph == None
    assert first.wind.as_dict() == {
        "code": None,
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": None, "units": "knot"},
        "speed": {"speed": None, "units": "knot"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None
