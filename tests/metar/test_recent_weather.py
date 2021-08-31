from aeromet_py import Metar


def test_recent_weather_first():
    metar = Metar("METAR MRLM 192300Z 05010KT 5000 +DZ FEW010 OVC080 24/23 A2987 RERA")
    recent_weather = metar.recent_weather

    assert recent_weather.description == None
    assert recent_weather.precipitation == "rain"
    assert recent_weather.obscuration == None
    assert recent_weather.other == None


def test_recent_weather_first():
    metar = Metar(
        "METAR SKBO 200800Z 36004KT 5000 RA FEW017 SCT070 10/09 Q1025 RETSGR NOSIG RMK A3029"
    )
    recent_weather = metar.recent_weather

    assert recent_weather.description == "thunderstorm"
    assert recent_weather.precipitation == "hail"
    assert recent_weather.obscuration == None
    assert recent_weather.other == None
