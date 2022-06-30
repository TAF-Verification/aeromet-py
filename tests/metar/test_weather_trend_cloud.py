import pytest

from aeromet_py import Metar
from aeromet_py.models.errors import RangeError

_year: int = 2019
_month: int = 7


def test_two_trend_cloud_layers():
    metar = Metar(
        "METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016 BECMG 5000 RA SCT010 BKN015",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG 5000 RA SCT010 BKN015"]
    assert (
        str(trends) == "becoming from 2019-07-19 08:00:00 until 2019-07-19 10:00:00\n"
        "5.0 km\n"
        "rain\n"
        "scattered at 1000.0 feet\n"
        "broken at 1500.0 feet"
    )

    first = trends[0]
    assert first.code == "BECMG 5000 RA SCT010 BKN015"

    clouds = first.clouds
    assert clouds.codes == ["SCT010", "BKN015"]
    assert str(clouds) == "scattered at 1000.0 feet | broken at 1500.0 feet"
    assert clouds.ceiling == True
    assert clouds.as_dict() == {
        "first": {
            "code": "SCT010",
            "cover": "scattered",
            "height": 304.8,
            "height_units": "meters",
            "oktas": "3-4",
            "type": None,
        },
        "second": {
            "code": "BKN015",
            "cover": "broken",
            "height": 457.2,
            "height_units": "meters",
            "oktas": "5-7",
            "type": None,
        },
    }

    assert clouds[0].code == "SCT010"
    assert clouds[0].cover == "scattered"
    assert clouds[0].oktas == "3-4"
    assert clouds[0].height_in_feet == 999.9999999999999
    assert clouds[0].height_in_meters == 304.8
    assert clouds[0].height_in_kilometers == 0.3048
    assert clouds[0].height_in_sea_miles == 0.16457883369330453
    assert clouds[0].cloud_type == None

    assert clouds[1].code == "BKN015"
    assert clouds[1].cover == "broken"
    assert clouds[1].oktas == "5-7"
    assert clouds[1].height_in_feet == 1499.9999999999998
    assert clouds[1].height_in_meters == 457.2
    assert clouds[1].height_in_kilometers == 0.4572
    assert clouds[1].height_in_sea_miles == 0.24686825053995676
    assert clouds[1].cloud_type == None

    with pytest.raises(IndexError):
        assert clouds[2].code == None


def test_three_layers():
    metar = Metar(
        "SPECI KMIA 191458Z 33006KT CAVOK 23/21 A3003 BECMG 5SM -TSRA BR FEW013 BKN021CB OVC040 RMK AO2 OCNL LTGICCG OHD TS OHD MOV SE P0007 T02280211",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG 5SM -TSRA BR FEW013 BKN021CB OVC040"]
    assert (
        str(trends) == "becoming from 2019-07-19 14:58:00 until 2019-07-19 16:58:00\n"
        "9.3 km\n"
        "light thunderstorm rain\n"
        "mist\n"
        "a few at 1300.0 feet\n"
        "broken at 2100.0 feet of cumulonimbus\n"
        "overcast at 4000.0 feet"
    )

    first = trends[0]
    assert first.code == "BECMG 5SM -TSRA BR FEW013 BKN021CB OVC040"

    clouds = first.clouds
    assert clouds.codes == ["FEW013", "BKN021CB", "OVC040"]
    assert (
        str(clouds)
        == "a few at 1300.0 feet | broken at 2100.0 feet of cumulonimbus | overcast at 4000.0 feet"
    )
    assert clouds.ceiling == False
    assert clouds.as_dict() == {
        "first": {
            "code": "FEW013",
            "cover": "a few",
            "height": 396.24,
            "height_units": "meters",
            "oktas": "1-2",
            "type": None,
        },
        "second": {
            "code": "BKN021CB",
            "cover": "broken",
            "height": 640.08,
            "height_units": "meters",
            "oktas": "5-7",
            "type": "cumulonimbus",
        },
        "third": {
            "code": "OVC040",
            "cover": "overcast",
            "height": 1219.2,
            "height_units": "meters",
            "oktas": "8",
            "type": None,
        },
    }

    assert clouds[0].code == "FEW013"
    assert clouds[0].cover == "a few"
    assert clouds[0].oktas == "1-2"
    assert clouds[0].height_in_feet == 1300.0
    assert clouds[0].height_in_meters == 396.24
    assert clouds[0].height_in_kilometers == 0.39624000000000004
    assert clouds[0].height_in_sea_miles == 0.21395248380129586
    assert clouds[0].cloud_type == None

    assert clouds[1].code == "BKN021CB"
    assert clouds[1].cover == "broken"
    assert clouds[1].oktas == "5-7"
    assert clouds[1].height_in_feet == 2100.0
    assert clouds[1].height_in_meters == 640.08
    assert clouds[1].height_in_kilometers == 0.6400800000000001
    assert clouds[1].height_in_sea_miles == 0.34561555075593947
    assert clouds[1].cloud_type == "cumulonimbus"

    assert clouds[2].code == "OVC040"
    assert clouds[2].cover == "overcast"
    assert clouds[2].oktas == "8"
    assert clouds[2].height_in_feet == 3999.9999999999995
    assert clouds[2].height_in_meters == 1219.2
    assert clouds[2].height_in_kilometers == 1.2192
    assert clouds[2].height_in_sea_miles == 0.6583153347732181
    assert clouds[2].cloud_type == None

    with pytest.raises(RangeError):
        assert clouds[4].code == None


def test_no_trend_clouds():
    metar = Metar(
        "METAR MROC 190700Z 11009KT CAVOK 22/19 A2997 TEMPO 9999 RA",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO 9999 RA"]
    assert (
        str(trends) == "temporary from 2019-07-19 07:00:00 until 2019-07-19 09:00:00\n"
        "10.0 km\n"
        "rain"
    )

    first = trends[0]
    assert first.code == "TEMPO 9999 RA"

    clouds = first.clouds
    assert clouds.codes == []
    assert str(clouds) == ""
    assert clouds.as_dict() == {}

    for i in range(4):
        with pytest.raises(IndexError):
            assert clouds[i].code == None
