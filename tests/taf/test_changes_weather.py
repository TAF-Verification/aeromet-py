from pytest import raises

from aeromet_py import Taf


def test_changes_weather():
    code = """
    TAF OMDB 281700Z 2818/3000 26010KT CAVOK
        BECMG 2818/2820 20005KT 5000 DS
        BECMG 2904/2906 29012KT
        BECMG 2916/2918 18005KT
    """
    taf = Taf(code)
    changes = taf.changes_forecasted

    weathers0 = changes[0].weathers

    assert weathers0.codes == ["DS"]
    assert str(weathers0) == "dust storm"
    assert weathers0.as_dict() == {
        "first": {
            "code": "DS",
            "description": None,
            "intensity": None,
            "obscuration": None,
            "other": "dust storm",
            "precipitation": None,
        }
    }

    assert weathers0[0].intensity == None
    assert weathers0[0].description == None
    assert weathers0[0].precipitation == None
    assert weathers0[0].obscuration == None
    assert weathers0[0].other == "dust storm"

    with raises(IndexError):
        weathers0[1].code == None

    weathers1 = changes[1].weathers

    assert weathers1.codes == []
    assert str(weathers1) == ""
    assert weathers1.as_dict() == {}

    with raises(IndexError):
        weathers1[0].code == None
