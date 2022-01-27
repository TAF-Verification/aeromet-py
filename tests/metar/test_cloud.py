import pytest

from aeromet_py import Metar
from aeromet_py.models.errors import RangeError


def test_two_layers():
    metar = Metar("METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016")
    clouds = metar.clouds

    assert clouds.codes == ["FEW049", "BKN056"]
    assert str(clouds) == "a few at 4900.0 feet | broken at 5600.0 feet"
    assert clouds.ceiling == False

    assert clouds[0].code == "FEW049"
    assert clouds[0].cover == "a few"
    assert clouds[0].oktas == "1-2"
    assert clouds[0].height_in_feet == 4899.999999999999
    assert clouds[0].height_in_meters == 1493.52
    assert clouds[0].height_in_kilometers == 1.49352
    assert clouds[0].height_in_sea_miles == 0.8064362850971921
    assert clouds[0].cloud_type == None

    assert clouds[1].code == "BKN056"
    assert clouds[1].cover == "broken"
    assert clouds[1].oktas == "5-7"
    assert clouds[1].height_in_feet == 5600.0
    assert clouds[1].height_in_meters == 1706.88
    assert clouds[1].height_in_kilometers == 1.7068800000000002
    assert clouds[1].height_in_sea_miles == 0.9216414686825053
    assert clouds[1].cloud_type == None

    with pytest.raises(IndexError):
        assert clouds[2].code == None


def test_three_layers():
    metar = Metar(
        "METAR KMIA 191458Z 33006KT 5SM R09/1800V4500FT -TSRA BR FEW013 BKN021CB OVC040 23/21 A3003 RMK AO2 OCNL LTGICCG OHD TS OHD MOV SE P0007 T02280211"
    )
    clouds = metar.clouds

    assert clouds.codes == ["FEW013", "BKN021CB", "OVC040"]
    assert (
        str(clouds)
        == "a few at 1300.0 feet | broken at 2100.0 feet of cumulonimbus | overcast at 4000.0 feet"
    )
    assert clouds.ceiling == False

    assert clouds[0].code == "FEW013"
    assert clouds[0].cover == "a few"
    assert clouds[0].oktas == "1-2"
    assert clouds[0].height_in_feet == 1300.0
    assert clouds[0].height_in_meters == 396.24
    assert clouds[0].height_in_kilometers == 0.39624000000000004
    assert clouds[0].height_in_sea_miles == 0.21395248380129586
    assert clouds[0].cloud_type == None

    assert clouds[1].code == "BKN021CB"
    assert clouds[1].cover == "broken"
    assert clouds[1].oktas == "5-7"
    assert clouds[1].height_in_feet == 2100.0
    assert clouds[1].height_in_meters == 640.08
    assert clouds[1].height_in_kilometers == 0.6400800000000001
    assert clouds[1].height_in_sea_miles == 0.34561555075593947
    assert clouds[1].cloud_type == "cumulonimbus"

    assert clouds[2].code == "OVC040"
    assert clouds[2].cover == "overcast"
    assert clouds[2].oktas == "8"
    assert clouds[2].height_in_feet == 3999.9999999999995
    assert clouds[2].height_in_meters == 1219.2
    assert clouds[2].height_in_kilometers == 1.2192
    assert clouds[2].height_in_sea_miles == 0.6583153347732181
    assert clouds[2].cloud_type == None

    with pytest.raises(RangeError):
        assert clouds[4].code == None


def test_no_clouds():
    metar = Metar("METAR MROC 190700Z 11009KT CAVOK 22/19 A2997 NOSIG")
    clouds = metar.clouds

    assert clouds.codes == []
    assert str(clouds) == ""

    for i in range(4):
        with pytest.raises(IndexError):
            assert clouds[i].code == None


def test_vertical_visibility():
    metar = Metar("METAR BIHN 051900Z AUTO 33008KT 1000 +SN VV/// M02/M04 Q1006")
    clouds = metar.clouds

    assert clouds.codes == ["VV///"]
    assert str(clouds) == "indefinite ceiling"
    assert clouds.ceiling == False

    assert clouds[0].code == "VV///"
    assert clouds[0].cover == "indefinite ceiling"
    assert clouds[0].oktas == "undefined"
    assert clouds[0].height_in_feet == None
    assert clouds[0].height_in_meters == None
    assert clouds[0].height_in_kilometers == None
    assert clouds[0].height_in_sea_miles == None
    assert clouds[0].cloud_type == None

    for i in range(1, 3):
        with pytest.raises(IndexError):
            assert clouds[i].code == None


def test_vertical_visibility_with_height():
    metar = Metar("METAR BIHN 051900Z AUTO 33008KT 1000 +SN VV005 M02/M04 Q1006")
    clouds = metar.clouds

    assert clouds.codes == ["VV005"]
    assert str(clouds) == "indefinite ceiling at 500.0 feet"
    assert clouds.ceiling == False

    assert clouds[0].code == "VV005"
    assert clouds[0].cover == "indefinite ceiling"
    assert clouds[0].oktas == "undefined"
    assert clouds[0].height_in_feet == 499.99999999999994
    assert clouds[0].height_in_meters == 152.4
    assert clouds[0].height_in_kilometers == 0.1524
    assert clouds[0].height_in_sea_miles == 0.08228941684665227
    assert clouds[0].cloud_type == None

    for i in range(1, 3):
        with pytest.raises(IndexError):
            assert clouds[i].code == None
