import pytest
from pytest import approx

from aeromet_py import Taf


def test_cloud_layers():
    code = """
    TAF RPMD 021100Z 0212/0312 36008KT 9999 FEW016TCU SCT090 BKN260
        TEMPO 0212/0218 03011KT 9000 -RA SCT015CB BKN090
    """
    taf = Taf(code)
    clouds = taf.clouds

    assert clouds.codes == ["FEW016TCU", "SCT090", "BKN260"]
    assert (
        str(clouds)
        == "a few at 1600.0 feet of towering cumulus | scattered at 9000.0 feet | broken at 26000.0 feet"
    )
    assert clouds.ceiling == False
    assert clouds.as_dict() == {
        "first": {
            "code": "FEW016TCU",
            "cover": "a few",
            "height": 487.68,
            "height_units": "meters",
            "oktas": "1-2",
            "type": "towering cumulus",
        },
        "second": {
            "code": "SCT090",
            "cover": "scattered",
            "height": 2743.2,
            "height_units": "meters",
            "oktas": "3-4",
            "type": None,
        },
        "third": {
            "code": "BKN260",
            "cover": "broken",
            "height": 7924.8,
            "height_units": "meters",
            "oktas": "5-7",
            "type": None,
        },
    }

    assert clouds[0].code == "FEW016TCU"
    assert clouds[0].cover == "a few"
    assert clouds[0].oktas == "1-2"
    assert clouds[0].height_in_feet == approx(1600.0)
    assert clouds[0].height_in_meters == 487.68
    assert clouds[0].height_in_kilometers == 0.48768
    assert clouds[0].height_in_sea_miles == 0.2633261339092872
    assert clouds[0].cloud_type == "towering cumulus"

    assert clouds[1].code == "SCT090"
    assert clouds[1].cover == "scattered"
    assert clouds[1].oktas == "3-4"
    assert clouds[1].height_in_feet == approx(9000.0)
    assert clouds[1].height_in_meters == 2743.2
    assert clouds[1].height_in_kilometers == 2.7432
    assert clouds[1].height_in_sea_miles == 1.4812095032397405
    assert clouds[1].cloud_type == None

    assert clouds[2].code == "BKN260"
    assert clouds[2].cover == "broken"
    assert clouds[2].oktas == "5-7"
    assert clouds[2].height_in_feet == approx(26000.0)
    assert clouds[2].height_in_meters == 7924.8
    assert clouds[2].height_in_kilometers == 7.9248
    assert clouds[2].height_in_sea_miles == 4.279049676025918
    assert clouds[2].cloud_type == None

    with pytest.raises(IndexError):
        assert clouds[3].code == None
