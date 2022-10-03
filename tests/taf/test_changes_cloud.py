from pytest import raises, approx

from aeromet_py import Taf


def test_changes_clouds():
    code = """
    TAF FMEE 281700Z 2818/2924 14006KT 9999 FEW030 BKN060
        PROB40
        TEMPO 2818/2921 4000 SHRA SCT020TCU BKN030
        BECMG 2922/2924 RA BKN010
    """
    taf = Taf(code)
    changes = taf.changes_forecasted

    clouds0 = changes[0].clouds
    assert clouds0.codes == ["SCT020TCU", "BKN030"]
    assert (
        str(clouds0)
        == "scattered at 2000.0 feet of towering cumulus | broken at 3000.0 feet"
    )
    assert clouds0.ceiling == False
    assert clouds0.as_dict() == {
        "first": {
            "code": "SCT020TCU",
            "cover": "scattered",
            "height": 609.6,
            "height_units": "meters",
            "oktas": "3-4",
            "type": "towering cumulus",
        },
        "second": {
            "code": "BKN030",
            "cover": "broken",
            "height": 914.4,
            "height_units": "meters",
            "oktas": "5-7",
            "type": None,
        },
    }

    assert clouds0[0].code == "SCT020TCU"
    assert clouds0[0].cover == "scattered"
    assert clouds0[0].oktas == "3-4"
    assert clouds0[0].height_in_feet == approx(2000.0)
    assert clouds0[0].height_in_meters == 609.6
    assert clouds0[0].height_in_kilometers == 0.6096
    assert clouds0[0].height_in_sea_miles == 0.32915766738660907
    assert clouds0[0].cloud_type == "towering cumulus"

    assert clouds0[1].code == "BKN030"
    assert clouds0[1].cover == "broken"
    assert clouds0[1].oktas == "5-7"
    assert clouds0[1].height_in_feet == approx(3000.0)
    assert clouds0[1].height_in_meters == 914.4
    assert clouds0[1].height_in_kilometers == 0.9144
    assert clouds0[1].height_in_sea_miles == 0.4937365010799135
    assert clouds0[1].cloud_type == None

    with raises(IndexError):
        assert clouds0[2].code == None

    clouds1 = changes[1].clouds

    assert clouds1.codes == ["BKN010"]
    assert str(clouds1) == "broken at 1000.0 feet"
    assert clouds1.ceiling == True
    assert clouds1.as_dict() == {
        "first": {
            "code": "BKN010",
            "cover": "broken",
            "height": 304.8,
            "height_units": "meters",
            "oktas": "5-7",
            "type": None,
        }
    }

    assert clouds1[0].code == "BKN010"
    assert clouds1[0].cover == "broken"
    assert clouds1[0].oktas == "5-7"
    assert clouds1[0].height_in_feet == approx(1000.0)
    assert clouds1[0].height_in_meters == 304.8
    assert clouds1[0].height_in_kilometers == 0.3048
    assert clouds1[0].height_in_sea_miles == 0.16457883369330453
    assert clouds1[0].cloud_type == None

    with raises(IndexError):
        assert clouds1[1].code == None
