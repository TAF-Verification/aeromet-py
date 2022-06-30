from aeromet_py import Metar


def test_recent_weather_first():
    metar = Metar("METAR MRLM 192300Z 05010KT 5000 +DZ FEW010 OVC080 24/23 A2987 RERA")
    recent_weather = metar.recent_weather

    assert recent_weather.code == "RERA"
    assert recent_weather.description == None
    assert recent_weather.precipitation == "rain"
    assert recent_weather.obscuration == None
    assert recent_weather.other == None
    assert str(recent_weather) == "rain"
    assert recent_weather.as_dict() == {
        "code": "RERA",
        "description": None,
        "obscuration": None,
        "other": None,
        "precipitation": "rain",
    }


def test_recent_weather_second():
    metar = Metar(
        "METAR SKBO 200800Z 36004KT 5000 RA FEW017 SCT070 10/09 Q1025 RETSGR NOSIG RMK A3029"
    )
    recent_weather = metar.recent_weather

    assert recent_weather.code == "RETSGR"
    assert recent_weather.description == "thunderstorm"
    assert recent_weather.precipitation == "hail"
    assert recent_weather.obscuration == None
    assert recent_weather.other == None
    assert str(recent_weather) == "thunderstorm hail"
    assert recent_weather.as_dict() == {
        "code": "RETSGR",
        "description": "thunderstorm",
        "obscuration": None,
        "other": None,
        "precipitation": "hail",
    }


def test_no_recent_weather():
    metar = Metar("METAR MRPV 160000Z 32006KT 4000 TSRA OVC008CB 20/20 A3002 NOSIG")
    recent_weather = metar.recent_weather

    assert recent_weather.code == None
    assert recent_weather.description == None
    assert recent_weather.precipitation == None
    assert recent_weather.obscuration == None
    assert recent_weather.other == None
    assert str(recent_weather) == ""
    assert recent_weather.as_dict() == {
        "code": None,
        "description": None,
        "obscuration": None,
        "other": None,
        "precipitation": None,
    }
