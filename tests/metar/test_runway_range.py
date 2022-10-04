import pytest
from pytest import approx

from aeromet_py import Metar
from aeromet_py.reports.models import RangeError


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
    assert ranges[0].as_dict() == {
        "code": "R07L/M0150V0600U",
        "high_range": {"distance": 600.0, "units": "meters"},
        "low_range": {"distance": 150.0, "units": "meters"},
        "name": "07 left",
        "rvr_high": None,
        "rvr_low": "below of",
        "trend": "increasing",
    }

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
    assert ranges[0].as_dict() == {
        "code": "R25C/P0150D",
        "high_range": {"distance": None, "units": "meters"},
        "low_range": {"distance": 150.0, "units": "meters"},
        "name": "25 center",
        "rvr_high": None,
        "rvr_low": "above of",
        "trend": "decreasing",
    }

    with pytest.raises(IndexError):
        ranges[1].code = None


def test_runway_range_in_feet():
    metar = Metar(
        "SPECI KMIA 280558Z 16010G20KT 5SM R09/5000VP6000FT -RA BR SCT020 BKN035CB OVC060 26/24 A2973 RMK AO2 WSHFT 0544 LTG DSNT NW CB W-N MOV NW P0009 T02610244"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R09/5000VP6000FT"]

    assert ranges[0].code == "R09/5000VP6000FT"
    assert ranges[0].low_in_meters == 1524.0
    assert ranges[0].low_in_kilometers == 1.524
    assert ranges[0].low_in_sea_miles == approx(0.822894)
    assert ranges[0].low_in_feet == approx(5000.0)
    assert ranges[0].high_in_meters == approx(1828.8)
    assert ranges[0].high_in_kilometers == approx(1.8288)
    assert ranges[0].high_in_sea_miles == approx(0.987473)
    assert ranges[0].high_in_feet == approx(6000.0)
    assert ranges[0].name == "09"
    assert ranges[0].low_range == "1524.0 m"
    assert ranges[0].high_range == "above of 1828.8 m"
    assert str(ranges[0]) == "runway 09 1524.0 m varying to above of 1828.8 m"
    assert ranges[0].as_dict() == {
        "code": "R09/5000VP6000FT",
        "high_range": {"distance": 1828.8000000000002, "units": "meters"},
        "low_range": {"distance": 1524.0, "units": "meters"},
        "name": "09",
        "rvr_high": "above of",
        "rvr_low": None,
        "trend": None,
    }

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
    assert ranges[0].as_dict() == {
        "code": "R07L/M0150V0600U",
        "high_range": {"distance": 600.0, "units": "meters"},
        "low_range": {"distance": 150.0, "units": "meters"},
        "name": "07 left",
        "rvr_high": None,
        "rvr_low": "below of",
        "trend": "increasing",
    }

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
    assert ranges[1].as_dict() == {
        "code": "R25C/P0150D",
        "high_range": {"distance": None, "units": "meters"},
        "low_range": {"distance": 150.0, "units": "meters"},
        "name": "25 center",
        "rvr_high": None,
        "rvr_low": "above of",
        "trend": "decreasing",
    }

    with pytest.raises(IndexError):
        ranges[2].code = None


def test_no_runway_range():
    metar = Metar("METAR SCFA 121300Z 21008KT 9999 3000W TSRA FEW020 20/13 Q1014 NOSIG")
    ranges = metar.runway_ranges

    assert ranges.codes == []
    assert str(ranges) == ""
    assert ranges.as_dict() == {}

    for i in range(3):
        with pytest.raises(IndexError):
            assert ranges[i].code == None


def test_try_to_get_item_4():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U R25C/P0150D R25L/P0500N TSRA FEW020 20/13 Q1014 NOSIG"
    )
    ranges = metar.runway_ranges

    assert ranges.codes == ["R07L/M0150V0600U", "R25C/P0150D", "R25L/P0500N"]
    assert (
        str(ranges) == "runway 07 left below of 150.0 m varying to 600.0 m, increasing "
        "| runway 25 center above of 150.0 m, decreasing "
        "| runway 25 left above of 500.0 m, no change"
    )
    assert ranges.as_dict() == {
        "first": {
            "code": "R07L/M0150V0600U",
            "high_range": {"distance": 600.0, "units": "meters"},
            "low_range": {"distance": 150.0, "units": "meters"},
            "name": "07 left",
            "rvr_high": None,
            "rvr_low": "below of",
            "trend": "increasing",
        },
        "second": {
            "code": "R25C/P0150D",
            "high_range": {"distance": None, "units": "meters"},
            "low_range": {"distance": 150.0, "units": "meters"},
            "name": "25 center",
            "rvr_high": None,
            "rvr_low": "above of",
            "trend": "decreasing",
        },
        "third": {
            "code": "R25L/P0500N",
            "high_range": {"distance": None, "units": "meters"},
            "low_range": {"distance": 500.0, "units": "meters"},
            "name": "25 left",
            "rvr_high": None,
            "rvr_low": "above of",
            "trend": "no change",
        },
    }

    with pytest.raises(RangeError):
        assert ranges[3].code == None
