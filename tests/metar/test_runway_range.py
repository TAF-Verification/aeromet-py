from aeromet_py import Metar


def test_runway_range():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U TSRA FEW020 20/13 Q1014 NOSIG"
    )
    rwy_range = metar.runway_range

    assert rwy_range.low_in_meters == 150.0
    assert rwy_range.low_in_kilometers == 0.150
    assert rwy_range.low_in_sea_miles == 0.08099352051835852
    assert rwy_range.high_in_meters == 600.0
    assert rwy_range.high_in_kilometers == 0.600
    assert rwy_range.high_in_sea_miles == 0.3239740820734341
    assert rwy_range.name == "07 left"
    assert rwy_range.low_range == "below of 150.0 meters"
    assert rwy_range.high_range == "600.0 meters"
    assert (
        str(rwy_range)
        == "runway 07 left below of 150.0 meters varying to 600.0 meters, increasing"
    )


def test_runway_range_no_high():
    metar = Metar(
        "METAR SCFA 121300Z 21008KT 9999 3000W R25C/P0150D TSRA FEW020 20/13 Q1014 NOSIG"
    )
    rwy_range = metar.runway_range

    assert rwy_range.low_in_meters == 150.0
    assert rwy_range.low_in_kilometers == 0.150
    assert rwy_range.low_in_sea_miles == 0.08099352051835852
    assert rwy_range.high_in_meters == None
    assert rwy_range.high_in_kilometers == None
    assert rwy_range.high_in_sea_miles == None
    assert rwy_range.name == "25 center"
    assert rwy_range.low_range == "above of 150.0 meters"
    assert rwy_range.high_range == None
    assert str(rwy_range) == "runway 25 center above of 150.0 meters, decreasing"


def test_no_runway_range():
    metar = Metar("METAR SCFA 121300Z 21008KT 9999 3000W TSRA FEW020 20/13 Q1014 NOSIG")
    rwy_range = metar.runway_range

    assert rwy_range.low_in_meters == None
    assert rwy_range.low_in_kilometers == None
    assert rwy_range.low_in_sea_miles == None
    assert rwy_range.high_in_meters == None
    assert rwy_range.high_in_kilometers == None
    assert rwy_range.high_in_sea_miles == None
    assert rwy_range.name == None
    assert rwy_range.low_range == None
    assert rwy_range.high_range == None
    assert str(rwy_range) == ""
