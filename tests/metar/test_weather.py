import pytest

from aeromet_py import Metar
from aeromet_py.reports.models import RangeError


def test_one_weather():
    metar = Metar(
        "METAR UUDD 190430Z 35004MPS 8000 -SN FEW012 M01/M03 Q1009 R32L/590240 NOSIG"
    )
    weathers = metar.weathers

    assert weathers.codes == ["-SN"]
    assert str(weathers) == "light snow"
    assert weathers[0].intensity == "light"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "snow"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None
    assert weathers[0].as_dict() == {
        "code": "-SN",
        "description": None,
        "intensity": "light",
        "obscuration": None,
        "other": None,
        "precipitation": "snow",
    }

    with pytest.raises(IndexError):
        weathers[1].code = None


def test_two_weathers():
    metar = Metar(
        "METAR MRLM 191300Z 22005KT 6000 +DZ VCSH FEW010TCU OVC070 24/23 A2991 RERA"
    )
    weathers = metar.weathers

    assert weathers.codes == ["+DZ", "VCSH"]
    assert str(weathers) == "heavy drizzle | nearby showers"

    assert weathers[0].intensity == "heavy"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "drizzle"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None
    assert weathers[0].as_dict() == {
        "code": "+DZ",
        "description": None,
        "intensity": "heavy",
        "obscuration": None,
        "other": None,
        "precipitation": "drizzle",
    }

    assert weathers[1].intensity == "nearby"
    assert weathers[1].description == "showers"
    assert weathers[1].precipitation == None
    assert weathers[1].obscuration == None
    assert weathers[1].other == None
    assert weathers[1].as_dict() == {
        "code": "VCSH",
        "description": "showers",
        "intensity": "nearby",
        "obscuration": None,
        "other": None,
        "precipitation": None,
    }

    with pytest.raises(IndexError):
        weathers[2].code = None


def test_three_weathers():
    metar = Metar(
        "METAR BIBD 191100Z 03002KT 5000 -RA BR VCTS SCT008CB OVC020 04/03 Q1013"
    )
    weathers = metar.weathers

    assert weathers.codes == ["-RA", "BR", "VCTS"]
    assert str(weathers) == "light rain | mist | nearby thunderstorm"

    assert weathers[0].intensity == "light"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "rain"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None
    assert weathers[0].as_dict() == {
        "code": "-RA",
        "description": None,
        "intensity": "light",
        "obscuration": None,
        "other": None,
        "precipitation": "rain",
    }

    assert weathers[1].intensity == None
    assert weathers[1].description == None
    assert weathers[1].precipitation == None
    assert weathers[1].obscuration == "mist"
    assert weathers[1].other == None
    assert weathers[1].as_dict() == {
        "code": "BR",
        "description": None,
        "intensity": None,
        "obscuration": "mist",
        "other": None,
        "precipitation": None,
    }

    assert weathers[2].intensity == "nearby"
    assert weathers[2].description == "thunderstorm"
    assert weathers[2].precipitation == None
    assert weathers[2].obscuration == None
    assert weathers[2].other == None
    assert weathers[2].as_dict() == {
        "code": "VCTS",
        "description": "thunderstorm",
        "intensity": "nearby",
        "obscuration": None,
        "other": None,
        "precipitation": None,
    }


def test_no_weathers():
    metar = Metar(
        "METAR LIRG 211755Z 27003KT CAVOK 24/14 Q1020 RMK FEW FEW200 MON NE LIB NC VIS MIN 9999 BLU"
    )
    weathers = metar.weathers

    assert weathers.codes == []
    assert str(weathers) == ""
    assert weathers.as_dict() == {}

    for i in range(3):
        with pytest.raises(IndexError):
            assert weathers[i].code == None


def test_try_to_get_item_4():
    metar = Metar(
        "METAR SCVM 060000Z 28007KT 250V310 9999 RA BR VCTS SCT016CB 16/13 Q1014"
    )
    weathers = metar.weathers

    assert weathers.codes == ["RA", "BR", "VCTS"]
    assert str(weathers) == "rain | mist | nearby thunderstorm"
    assert weathers.as_dict() == {
        "first": {
            "code": "RA",
            "description": None,
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
            "code": "VCTS",
            "description": "thunderstorm",
            "intensity": "nearby",
            "obscuration": None,
            "other": None,
            "precipitation": None,
        },
    }

    with pytest.raises(RangeError):
        assert weathers[3].code == None
