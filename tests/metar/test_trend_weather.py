import pytest

from aeromet_py import Metar
from aeromet_py.models import RangeError


def test_one_trend_weather():
    metar = Metar(
        "METAR UUDD 190430Z 35004MPS 9999 FEW020 M01/M03 Q1009 R32L/590240 TEMPO TL0600 5000 +SN SCT012"
    )
    weathers = metar.trend_weathers

    assert weathers.codes == ["+SN"]
    assert weathers[0].intensity == "heavy"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "snow"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None
    assert str(weathers) == "heavy snow"

    with pytest.raises(IndexError):
        weathers[1].code = None


def test_two_trend_weathers():
    metar = Metar(
        "METAR MRLM 191300Z 22005KT 6000 +DZ VCSH FEW010TCU OVC070 24/23 A2991 RERA BECMG 3000 TSRA BR SCT010CB"
    )
    weathers = metar.trend_weathers

    assert weathers.codes == ["TSRA", "BR"]
    assert str(weathers) == "thunderstorm rain | mist"

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


def test_three_trend_weathers():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 9999 SCT008CB OVC020 04/03 Q1013 TEMPO 5000 -RA BR VCTS"
    )
    weathers = metar.trend_weathers

    assert weathers.codes == ["-RA", "BR", "VCTS"]
    assert str(weathers) == "light rain | mist | nearby thunderstorm"

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


def test_no_weathers():
    metar = Metar(
        "METAR LIRG 211755Z 27003KT CAVOK 24/14 Q1020 NOSIG RMK FEW FEW200 MON NE LIB NC VIS MIN 9999 BLU"
    )
    weathers = metar.trend_weathers

    assert weathers.codes == []
    assert str(weathers) == ""

    for i in range(3):
        with pytest.raises(IndexError):
            assert weathers[i].code == None


def test_try_to_get_item_4_in_trend_weathers():
    metar = Metar(
        "METAR SCVM 060000Z 28007KT 250V310 9999 SCT016CB 16/13 Q1014 BECMG 5000 TSRA BR VCFG"
    )
    weathers = metar.trend_weathers

    assert weathers.codes == ["TSRA", "BR", "VCFG"]
    assert str(weathers) == "thunderstorm rain | mist | nearby fog"

    with pytest.raises(RangeError):
        assert weathers[3].code == None
