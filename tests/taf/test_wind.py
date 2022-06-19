from pytest import approx

from aeromet_py import Taf


def test_wind_in_mps():
    code = """
    TAF ULAA 281700Z 2818/0118 24004G09MPS 9999 SCT016
        TEMPO 2818/2823 23005G13MPS 6000 -SHSN FEW007 BKN016CB
        FM282300 22003G10MPS 6000 FEW005 BKN016
        TEMPO 0102/0115 18003MPS
    """
    taf = Taf(code)
    wind = taf.wind

    assert wind.code == "24004G09MPS"
    assert wind.cardinal_direction == "WSW"
    assert wind.direction_in_degrees == 240.0
    assert wind.direction_in_radians == 4.1887902047863905
    assert wind.variable == False
    assert wind.speed_in_knot == 7.775378036936312
    assert wind.speed_in_mps == 4.0
    assert wind.speed_in_kph == 14.40000012440605
    assert wind.gust_in_knot == 17.494600583106703
    assert wind.gust_in_mps == approx(9.0)
    assert wind.gust_in_miph == 20.13243645902753
    assert str(wind) == "WSW (240.0°) 7.8 kt gust of 17.5 kt"
