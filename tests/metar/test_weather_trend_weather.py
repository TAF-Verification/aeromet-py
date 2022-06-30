import pytest

from aeromet_py import Metar
from aeromet_py.models import RangeError

_year: int = 2020
_month: int = 10


def test_one_weather_trend_weather():
    metar = Metar(
        "SPECI UUDD 190430Z 35004MPS 9999 FEW020 M01/M03 Q1009 R32L/590240 TEMPO TL0600 5000 +SN SCT012",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO TL0600 5000 +SN SCT012"]
    assert (
        str(trends) == "temporary from 2020-10-19 04:30:00 until 2020-10-19 06:00:00\n"
        "5.0 km\n"
        "heavy snow\n"
        "scattered at 1200.0 feet"
    )

    first = trends[0]
    assert first.code == "TEMPO TL0600 5000 +SN SCT012"

    weathers = first.weathers

    assert weathers.codes == ["+SN"]
    assert str(weathers) == "heavy snow"
    assert weathers.as_dict() == {
        "first": {
            "code": "+SN",
            "description": None,
            "intensity": "heavy",
            "obscuration": None,
            "other": None,
            "precipitation": "snow",
        }
    }

    assert weathers[0].intensity == "heavy"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "snow"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None
    assert str(weathers) == "heavy snow"

    with pytest.raises(IndexError):
        weathers[1].code = None


def test_two_weather_trend_weathers():
    metar = Metar(
        "METAR MRLM 191300Z 22005KT 6000 +DZ VCSH FEW010TCU OVC070 24/23 A2991 RERA BECMG 3000 TSRA BR SCT010CB",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG 3000 TSRA BR SCT010CB"]
    assert (
        str(trends) == "becoming from 2020-10-19 13:00:00 until 2020-10-19 15:00:00\n"
        "3.0 km\n"
        "thunderstorm rain\n"
        "mist\n"
        "scattered at 1000.0 feet of cumulonimbus"
    )

    first = trends[0]
    assert first.code == "BECMG 3000 TSRA BR SCT010CB"

    weathers = first.weathers

    assert weathers.codes == ["TSRA", "BR"]
    assert str(weathers) == "thunderstorm rain | mist"
    assert weathers.as_dict() == {
        "first": {
            "code": "TSRA",
            "description": "thunderstorm",
            "intensity": None,
            "obscuration": None,
            "other": None,
            "precipitation": "rain",
        },
        "second": {
            "code": "BR",
            "description": None,
            "intensity": None,
            "obscuration": "mist",
            "other": None,
            "precipitation": None,
        },
    }

    assert weathers[0].intensity == None
    assert weathers[0].description == "thunderstorm"
    assert weathers[0].precipitation == "rain"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None

    assert weathers[1].intensity == None
    assert weathers[1].description == None
    assert weathers[1].precipitation == None
    assert weathers[1].obscuration == "mist"
    assert weathers[1].other == None

    with pytest.raises(IndexError):
        weathers[2].code = None


def test_three_weather_trend_weathers():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 9999 SCT008CB OVC020 04/03 Q1013 TEMPO 5000 -RA BR VCTS",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO 5000 -RA BR VCTS"]
    assert (
        str(trends) == "temporary from 2020-10-19 11:00:00 until 2020-10-19 13:00:00\n"
        "5.0 km\n"
        "light rain\n"
        "mist\n"
        "nearby thunderstorm"
    )

    first = trends[0]
    assert first.code == "TEMPO 5000 -RA BR VCTS"

    weathers = first.weathers

    assert weathers.codes == ["-RA", "BR", "VCTS"]
    assert str(weathers) == "light rain | mist | nearby thunderstorm"
    assert weathers.as_dict() == {
        "first": {
            "code": "-RA",
            "description": None,
            "intensity": "light",
            "obscuration": None,
            "other": None,
            "precipitation": "rain",
        },
        "second": {
            "code": "BR",
            "description": None,
            "intensity": None,
            "obscuration": "mist",
            "other": None,
            "precipitation": None,
        },
        "third": {
            "code": "VCTS",
            "description": "thunderstorm",
            "intensity": "nearby",
            "obscuration": None,
            "other": None,
            "precipitation": None,
        },
    }

    assert weathers[0].intensity == "light"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "rain"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None

    assert weathers[1].intensity == None
    assert weathers[1].description == None
    assert weathers[1].precipitation == None
    assert weathers[1].obscuration == "mist"
    assert weathers[1].other == None

    assert weathers[2].intensity == "nearby"
    assert weathers[2].description == "thunderstorm"
    assert weathers[2].precipitation == None
    assert weathers[2].obscuration == None
    assert weathers[2].other == None


def test_no_weather_trend_weathers():
    metar = Metar(
        "METAR LIRG 211755Z 27003KT CAVOK 24/14 Q1020 NOSIG RMK FEW FEW200 MON NE LIB NC VIS MIN 9999 BLU",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["NOSIG"]
    assert (
        str(trends)
        == "no significant changes from 2020-10-21 17:55:00 until 2020-10-21 19:55:00"
    )

    first = trends[0]
    assert first.code == "NOSIG"

    weathers = first.weathers
    assert weathers.codes == []
    assert str(weathers) == ""
    assert weathers.as_dict() == {}

    for i in range(3):
        with pytest.raises(IndexError):
            assert weathers[i].code == None


def test_try_to_get_item_4_in_weather_trend_weathers():
    metar = Metar(
        "METAR SCVM 060000Z 28007KT 250V310 9999 SCT016CB 16/13 Q1014 BECMG 5000 TSRA BR VCFG",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends
    first = trends[0]

    weathers = first.weathers
    assert weathers.codes == ["TSRA", "BR", "VCFG"]
    assert str(weathers) == "thunderstorm rain | mist | nearby fog"
    assert weathers.as_dict() == {
        "first": {
            "code": "TSRA",
            "description": "thunderstorm",
            "intensity": None,
            "obscuration": None,
            "other": None,
            "precipitation": "rain",
        },
        "second": {
            "code": "BR",
            "description": None,
            "intensity": None,
            "obscuration": "mist",
            "other": None,
            "precipitation": None,
        },
        "third": {
            "code": "VCFG",
            "description": None,
            "intensity": "nearby",
            "obscuration": "fog",
            "other": None,
            "precipitation": None,
        },
    }

    with pytest.raises(RangeError):
        assert weathers[3].code == None
