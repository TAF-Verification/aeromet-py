from aeromet_py import Metar


def test_trend_no_time_groups():
    metar = Metar(
        "METAR MRPV 091700Z COR 07005KT 9999 BKN045 27/17 A3003 BECMG 29005KT"
    )
    trend = metar.trend

    assert trend.codes == ("BECMG",)
    assert trend.trend == "becoming"
    assert trend.from_time == None
    assert trend.until_time == None
    assert trend.at_time == None
    assert str(trend) == "becoming"


def test_trend_with_from_group():
    metar = Metar(
        "METAR LFOT 090330Z AUTO 04006KT 360V070 CAVOK 11/09 Q1023 BECMG FM0400 1400 BR OVC003"
    )
    trend = metar.trend

    assert trend.codes == ("BECMG", "FM0400")
    assert trend.trend == "becoming"
    assert trend.from_time == "04:00Z"
    assert trend.until_time == None
    assert trend.at_time == None
    assert str(trend) == "becoming from 04:00Z"


def test_trend_with_from_and_until_groups():
    metar = Metar(
        "METAR LFOT 090330Z AUTO 04006KT 360V070 CAVOK 11/09 Q1023 TEMPO FM0400 TL0630 1400 BR OVC003"
    )
    trend = metar.trend

    assert trend.codes == ("TEMPO", "FM0400", "TL0630")
    assert trend.trend == "temporary"
    assert trend.from_time == "04:00Z"
    assert trend.until_time == "06:30Z"
    assert trend.at_time == None
    assert str(trend) == "temporary from 04:00Z until 06:30Z"


def test_trend_with_at_group():
    metar = Metar(
        "METAR LFOT 090330Z AUTO 04006KT 360V070 CAVOK 11/09 Q1023 BECMG AT0400 1400 BR OVC003"
    )
    trend = metar.trend

    assert trend.codes == ("BECMG", "AT0400")
    assert trend.trend == "becoming"
    assert trend.from_time == None
    assert trend.until_time == None
    assert trend.at_time == "04:00Z"
    assert str(trend) == "becoming at 04:00Z"
