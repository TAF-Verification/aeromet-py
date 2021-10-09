from aeromet_py.models import weather
from aeromet_py import Metar


def test_one_weather():
    metar = Metar(
        "METAR UUDD 190430Z 35004MPS 8000 -SN FEW012 M01/M03 Q1009 R32L/590240 NOSIG"
    )
    weathers = metar.weathers

    assert weathers.first.intensity == "light"
    assert weathers.first.description == None
    assert weathers.first.precipitation == "snow"
    assert weathers.first.obscuration == None
    assert weathers.first.other == None
    assert str(weathers) == "light snow"


def test_two_weathers():
    metar = Metar(
        "METAR MRLM 191300Z 22005KT 6000 +DZ VCSH FEW010TCU OVC070 24/23 A2991 RERA"
    )
    weathers = metar.weathers

    assert weathers.first.intensity == "heavy"
    assert weathers.first.description == None
    assert weathers.first.precipitation == "drizzle"
    assert weathers.first.obscuration == None
    assert weathers.first.other == None

    assert weathers.second.intensity == "nearby"
    assert weathers.second.description == "showers"
    assert weathers.second.precipitation == None
    assert weathers.second.obscuration == None
    assert weathers.second.other == None

    assert str(weathers) == "heavy drizzle | nearby showers"


def test_three_weathers():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 5000 -RA BR VCTS SCT008CB OVC020 04/03 Q1013"
    )
    weathers = metar.weathers

    assert weathers.first.intensity == "light"
    assert weathers.first.description == None
    assert weathers.first.precipitation == "rain"
    assert weathers.first.obscuration == None
    assert weathers.first.other == None

    assert weathers.second.intensity == None
    assert weathers.second.description == None
    assert weathers.second.precipitation == None
    assert weathers.second.obscuration == "mist"
    assert weathers.second.other == None

    assert weathers.third.intensity == "nearby"
    assert weathers.third.description == "thunderstorm"
    assert weathers.third.precipitation == None
    assert weathers.third.obscuration == None
    assert weathers.third.other == None

    assert str(weathers) == "light rain | mist | nearby thunderstorm"


def test_no_weathers():
    metar = Metar(
        "METAR LIRG 211755Z 27003KT CAVOK 24/14 Q1020 RMK FEW FEW200 MON NE LIB NC VIS MIN 9999 BLU"
    )
    weathers = metar.weathers

    assert weathers.first.intensity == None
    assert weathers.first.description == None
    assert weathers.first.precipitation == None
    assert weathers.first.obscuration == None
    assert weathers.first.other == None

    assert weathers.second.intensity == None
    assert weathers.second.description == None
    assert weathers.second.precipitation == None
    assert weathers.second.obscuration == None
    assert weathers.second.other == None

    assert weathers.third.intensity == None
    assert weathers.third.description == None
    assert weathers.third.precipitation == None
    assert weathers.third.obscuration == None
    assert weathers.third.other == None

    assert str(weathers) == ""
