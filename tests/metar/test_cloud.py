import pytest

from typing import Literal

from aeromet_py import Metar as AeroMetar
from aeromet_py.reports.models import RangeError, Cloud, CloudList
from metar.Metar import Metar as PythonMetar
from metar.Datatypes import distance


class PythonMetarClouds:
    """Extract the clouds of a METAR using the python-metar module."""

    def __init__(self, code: str) -> None:
        metar: PythonMetar = PythonMetar(code)
        self.clouds: list[tuple[str, distance | None, str]] = metar.sky

    def get(
        self,
        index: Literal[0, 1, 2, 3] = 0,
    ) -> tuple[str, distance | None, str] | None:
        try:
            layer: tuple[str, distance | None, str] = self.clouds[index]
            return layer
        except IndexError:
            return None


covers: dict[str, str] = {
    "FEW": "a few",
    "SCT": "scattered",
    "BKN": "broken",
    "OVC": "overcast",
    "NSC": "no significant clouds",
    "VV": "vertical visibility",
    "SKC": "clear",
    "CLR": "clear",
}


def assert_cloud_layer(
    layer: Cloud,
    code: str,
    cover: str,
    oktas: str,
    height_feet: float,
    height_meters: float,
    height_kilometers: float,
    height_sea_miles: float,
    cloud_type: str | None,
    height_units: str = "meters",
) -> None:
    assert layer.code == code
    assert layer.cover == cover
    assert layer.oktas == oktas
    assert layer.height_in_feet == pytest.approx(height_feet)
    assert layer.height_in_meters == pytest.approx(height_meters)
    assert layer.height_in_kilometers == pytest.approx(height_kilometers)
    assert layer.height_in_sea_miles == pytest.approx(height_sea_miles)
    assert layer.cloud_type == cloud_type
    assert layer.as_dict() == {
        "code": code,
        "cover": cover,
        "height": height_meters,
        "height_units": height_units,
        "oktas": oktas,
        "type": cloud_type,
    }


def assert_index_error(collection, index: int):
    with pytest.raises(IndexError):
        _ = collection[index]


def test_get_layers():
    code = "METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016"
    python_metar_clouds = PythonMetarClouds(code=code)

    first: tuple[str, distance | None, str] | None = python_metar_clouds.get()
    second: tuple[str, distance | None, str] | None = python_metar_clouds.get(1)

    if first is not None:
        assert first[0] == "FEW"
    if second is not None:
        assert second[0] == "BKN"


def test_two_cloud_layers():
    metar: AeroMetar = AeroMetar(code="METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016")
    clouds: CloudList = metar.clouds

    assert clouds.codes == ["FEW049", "BKN056"]
    assert str(clouds) == "a few at 4900.0 feet | broken at 5600.0 feet"
    assert clouds.ceiling is False

    assert_cloud_layer(
        layer=clouds[0],
        code="FEW049",
        cover="a few",
        oktas="1-2",
        height_feet=4899.999999999999,
        height_meters=1493.52,
        height_kilometers=1.49352,
        height_sea_miles=0.8064362850971921,
        cloud_type=None,
    )

    assert_cloud_layer(
        layer=clouds[1],
        code="BKN056",
        cover="broken",
        oktas="5-7",
        height_feet=5600.0,
        height_meters=1706.88,
        height_kilometers=1.7068800000000002,
        height_sea_miles=0.9216414686825053,
        cloud_type=None,
    )

    assert_index_error(collection=clouds, index=2)


def test_three_cloud_layers():
    metar: AeroMetar = AeroMetar(
        code="METAR KMIA 191458Z 33006KT 5SM R09/1800V4500FT -TSRA BR FEW013 BKN021CB OVC040 23/21 A3003 RMK AO2 OCNL LTGICCG OHD TS OHD MOV SE P0007 T02280211"
    )
    clouds: CloudList = metar.clouds

    assert clouds.codes == ["FEW013", "BKN021CB", "OVC040"]
    assert (
        str(clouds)
        == "a few at 1300.0 feet | broken at 2100.0 feet of cumulonimbus | overcast at 4000.0 feet"
    )
    assert clouds.ceiling is False

    assert_cloud_layer(
        layer=clouds[0],
        code="FEW013",
        cover="a few",
        oktas="1-2",
        height_feet=1300.0,
        height_meters=396.24,
        height_kilometers=0.39624000000000004,
        height_sea_miles=0.21395248380129586,
        cloud_type=None,
    )

    assert_cloud_layer(
        layer=clouds[1],
        code="BKN021CB",
        cover="broken",
        oktas="5-7",
        height_feet=2100.0,
        height_meters=640.08,
        height_kilometers=0.6400800000000001,
        height_sea_miles=0.34561555075593947,
        cloud_type="cumulonimbus",
    )

    assert_cloud_layer(
        layer=clouds[2],
        code="OVC040",
        cover="overcast",
        oktas="8",
        height_feet=3999.9999999999995,
        height_meters=1219.2,
        height_kilometers=1.2192,
        height_sea_miles=0.6583153347732181,
        cloud_type=None,
    )

    with pytest.raises(RangeError):
        _ = clouds[4]


def test_no_clouds():
    metar: AeroMetar = AeroMetar("METAR MROC 190700Z 11009KT CAVOK 22/19 A2997 NOSIG")
    clouds: CloudList = metar.clouds

    assert clouds.codes == []
    assert str(clouds) == ""

    for i in range(4):
        assert_index_error(clouds, i)


def test_vertical_visibility():
    metar: AeroMetar = AeroMetar("METAR BIHN 051900Z AUTO 33008KT 1000 +SN VV/// M02/M04 Q1006")
    clouds: CloudList = metar.clouds

    assert clouds.codes == ["VV///"]
    assert str(clouds) == "indefinite ceiling"
    assert clouds.ceiling is False

    assert clouds[0].code == "VV///"
    assert clouds[0].cover == "indefinite ceiling"
    assert clouds[0].oktas == "undefined"
    assert clouds[0].height_in_feet is None
    assert clouds[0].height_in_meters is None
    assert clouds[0].height_in_kilometers is None
    assert clouds[0].height_in_sea_miles is None
    assert clouds[0].cloud_type is None
    assert clouds[0].as_dict() == {
        "code": "VV///",
        "cover": "indefinite ceiling",
        "height": None,
        "height_units": "meters",
        "oktas": "undefined",
        "type": None,
    }

    for i in range(1, 3):
        assert_index_error(clouds, i)


def test_vertical_visibility_with_height():
    metar: AeroMetar = AeroMetar("METAR BIHN 051900Z AUTO 33008KT 1000 +SN VV005 M02/M04 Q1006")
    clouds: CloudList = metar.clouds

    assert clouds.codes == ["VV005"]
    assert str(clouds) == "indefinite ceiling at 500.0 feet"
    assert clouds.ceiling is False

    assert clouds[0].code == "VV005"
    assert clouds[0].cover == "indefinite ceiling"
    assert clouds[0].oktas == "undefined"
    assert clouds[0].height_in_feet == pytest.approx(499.99999999999994)
    assert clouds[0].height_in_meters == pytest.approx(152.4)
    assert clouds[0].height_in_kilometers == pytest.approx(0.1524)
    assert clouds[0].height_in_sea_miles == pytest.approx(0.08228941684665227)
    assert clouds[0].cloud_type is None
    assert clouds[0].as_dict() == {
        "code": "VV005",
        "cover": "indefinite ceiling",
        "height": 152.4,
        "height_units": "meters",
        "oktas": "undefined",
        "type": None,
    }

    for i in range(1, 3):
        assert_index_error(clouds, i)
