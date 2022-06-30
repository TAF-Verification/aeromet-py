import pytest

from aeromet_py import Metar

_year: int = 2020
_month: int = 8


def test_weather_trend_visibility_from_meters():
    metar = Metar(
        "METAR SBBV 170400Z 08004KT 9999 SCT030 FEW035TCU BKN070 26/23 Q1012 BECMG 5000 +RA",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "BECMG 5000 +RA"
    assert first.prevailing_visibility.code == "5000"
    assert first.prevailing_visibility.in_meters == 5_000.0
    assert first.prevailing_visibility.in_kilometers == 5.0
    assert first.prevailing_visibility.in_sea_miles == 2.6997840172786174
    assert first.prevailing_visibility.in_feet == 16_404.199475065616
    assert first.prevailing_visibility.cavok == False
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == "5.0 km"
    assert first.prevailing_visibility.as_dict() == {
        "cavok": False,
        "code": "5000",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 5000.0, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_visibility_from_seamiles():
    metar = Metar(
        "SPECI PALH 170933Z 00000KT 10SM FEW020 M14/M16 A2980 TEMPO FM1000 TL1100 1 1/4SM BR BKN002 RMK AO2 T11441156"
    )
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "TEMPO FM1000 TL1100 1 1/4SM BR BKN002"
    assert first.prevailing_visibility.code == "1 1/4SM"
    assert first.prevailing_visibility.in_meters == 2315.0
    assert first.prevailing_visibility.in_kilometers == 2.315
    assert first.prevailing_visibility.in_sea_miles == 1.2499999999999998
    assert first.prevailing_visibility.in_feet == 7_595.144356955379
    assert first.prevailing_visibility.cavok == False
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == "2.3 km"
    assert first.prevailing_visibility.as_dict() == {
        "cavok": False,
        "code": "1 1/4SM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 2315.0, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_visibility_from_seamiles_only_fraction():
    metar = Metar(
        "METAR PALH 170933Z 00000KT 2SM BR FEW002 M14/M16 A2980 BECMG AT1000 1/2SM RMK AO2 T11441156"
    )
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "BECMG AT1000 1/2SM"
    assert first.prevailing_visibility.code == "1/2SM"
    assert first.prevailing_visibility.in_meters == 926.0
    assert first.prevailing_visibility.in_kilometers == 0.926
    assert first.prevailing_visibility.in_sea_miles == 0.49999999999999994
    assert first.prevailing_visibility.in_feet == 3038.0577427821518
    assert first.prevailing_visibility.cavok == False
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == "0.9 km"
    assert first.prevailing_visibility.as_dict() == {
        "cavok": False,
        "code": "1/2SM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 926.0, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_visibility_from_kilometers():
    metar = Metar("METAR SCAT 210900Z 18005KT 10KM OVC027/// 16/12 Q1013 BECMG 5KM")
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "BECMG 5KM"
    assert first.prevailing_visibility.code == "5KM"
    assert first.prevailing_visibility.in_meters == 5_000.0
    assert first.prevailing_visibility.in_kilometers == 5.0
    assert first.prevailing_visibility.in_sea_miles == 2.6997840172786174
    assert first.prevailing_visibility.in_feet == 16_404.199475065616
    assert first.prevailing_visibility.cavok == False
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == "5.0 km"
    assert first.prevailing_visibility.as_dict() == {
        "cavok": False,
        "code": "5KM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 5000.0, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_visibility_from_cavok():
    metar = Metar(
        "METAR SAAR 222000Z 13011KT 100V160 9999 FEW030 32/15 Q1012 BECMG AT2100 CAVOK RMK PP000"
    )
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "BECMG AT2100 CAVOK"
    assert first.prevailing_visibility.code == "CAVOK"
    assert first.prevailing_visibility.in_meters == 10_000.0
    assert first.prevailing_visibility.in_kilometers == 10.0
    assert first.prevailing_visibility.in_sea_miles == 5.399568034557235
    assert first.prevailing_visibility.in_feet == 32808.39895013123
    assert first.prevailing_visibility.cavok == True
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == "Ceiling and Visibility OK"
    assert first.prevailing_visibility.as_dict() == {
        "cavok": True,
        "code": "CAVOK",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 10000.0, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_no_weather_trend_visibility():
    metar = Metar(
        "METAR PALH 170933Z 00000KT BR FEW002 M14/M16 A2980 NOSIG RMK AO2 T11441156"
    )
    trends = metar.weather_trends

    first = trends[0]
    assert first.code == "NOSIG"
    assert first.prevailing_visibility.code == None
    assert first.prevailing_visibility.in_meters == None
    assert first.prevailing_visibility.in_kilometers == None
    assert first.prevailing_visibility.in_sea_miles == None
    assert first.prevailing_visibility.in_feet == None
    assert first.prevailing_visibility.cavok == False
    assert first.prevailing_visibility.cardinal_direction == None
    assert first.prevailing_visibility.direction_in_degrees == None
    assert first.prevailing_visibility.direction_in_radians == None
    assert str(first.prevailing_visibility) == ""
    assert first.prevailing_visibility.as_dict() == {
        "cavok": False,
        "code": None,
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": None, "units": "meters"},
    }

    with pytest.raises(IndexError):
        assert trends[1].code == None
