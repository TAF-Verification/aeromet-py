import pytest

from aeromet_py import Metar
from aeromet_py.models.errors import RangeError


def test_runway_range():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U TSRA FEW020 20/13 Q1014 NOSIG"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R07L/M0150V0600U"]

    assert ranges[0].code == "R07L/M0150V0600U"
    assert ranges[0].low_in_meters == 150.0
    assert ranges[0].low_in_kilometers == 0.150
    assert ranges[0].low_in_sea_miles == 0.08099352051835852
    assert ranges[0].low_in_feet == 492.1259842519685
    assert ranges[0].high_in_meters == 600.0
    assert ranges[0].high_in_kilometers == 0.600
    assert ranges[0].high_in_sea_miles == 0.3239740820734341
    assert ranges[0].high_in_feet == 1968.503937007874
    assert ranges[0].name == "07 left"
    assert ranges[0].low_range == "below of 150.0 m"
    assert ranges[0].high_range == "600.0 m"
    assert (
        str(ranges[0])
        == "runway 07 left below of 150.0 m varying to 600.0 m, increasing"
    )

    with pytest.raises(IndexError):
        ranges[1].code = None


def test_runway_range_no_high():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R25C/P0150D TSRA FEW020 20/13 Q1014 NOSIG"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R25C/P0150D"]

    assert ranges[0].code == "R25C/P0150D"
    assert ranges[0].low_in_meters == 150.0
    assert ranges[0].low_in_kilometers == 0.150
    assert ranges[0].low_in_sea_miles == 0.08099352051835852
    assert ranges[0].low_in_feet == 492.1259842519685
    assert ranges[0].high_in_meters == None
    assert ranges[0].high_in_kilometers == None
    assert ranges[0].high_in_sea_miles == None
    assert ranges[0].high_in_feet == None
    assert ranges[0].name == "25 center"
    assert ranges[0].low_range == "above of 150.0 m"
    assert ranges[0].high_range == ""
    assert str(ranges[0]) == "runway 25 center above of 150.0 m, decreasing"

    with pytest.raises(IndexError):
        ranges[1].code = None


def test_two_runway_ranges():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U R25C/P0150D TSRA FEW020 20/13 Q1014 NOSIG"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R07L/M0150V0600U", "R25C/P0150D"]

    assert ranges[0].code == "R07L/M0150V0600U"
    assert ranges[0].low_in_meters == 150.0
    assert ranges[0].low_in_kilometers == 0.150
    assert ranges[0].low_in_sea_miles == 0.08099352051835852
    assert ranges[0].high_in_meters == 600.0
    assert ranges[0].high_in_kilometers == 0.600
    assert ranges[0].high_in_sea_miles == 0.3239740820734341
    assert ranges[0].name == "07 left"
    assert ranges[0].low_range == "below of 150.0 m"
    assert ranges[0].high_range == "600.0 m"
    assert (
        str(ranges[0])
        == "runway 07 left below of 150.0 m varying to 600.0 m, increasing"
    )

    assert ranges[1].code == "R25C/P0150D"
    assert ranges[1].low_in_meters == 150.0
    assert ranges[1].low_in_kilometers == 0.150
    assert ranges[1].low_in_sea_miles == 0.08099352051835852
    assert ranges[1].high_in_meters == None
    assert ranges[1].high_in_kilometers == None
    assert ranges[1].high_in_sea_miles == None
    assert ranges[1].name == "25 center"
    assert ranges[1].low_range == "above of 150.0 m"
    assert ranges[1].high_range == ""
    assert str(ranges[1]) == "runway 25 center above of 150.0 m, decreasing"

    with pytest.raises(IndexError):
        ranges[2].code = None


def test_no_runway_range():
    metar = Metar("METAR SCFA 121300Z 21008KT 9999 3000W TSRA FEW020 20/13 Q1014 NOSIG")
    ranges = metar.runway_ranges

    assert ranges.codes == []
    assert str(ranges) == ""

    for i in range(3):
        with pytest.raises(IndexError):
            assert ranges[i].code == None


def test_try_to_get_item_4():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U R25C/P0150D R25L/P0500N TSRA FEW020 20/13 Q1014 NOSIG"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R07L/M0150V0600U", "R25C/P0150D", "R25L/P0500N"]

    with pytest.raises(RangeError):
        assert ranges[3].code == None
