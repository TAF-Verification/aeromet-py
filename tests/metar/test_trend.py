from aeromet_py import Metar

_year: int = 2022
_month: int = 2


def test_trend_code_nosig():
    metar = Metar(
        "METAR SEQM 050400Z 04010KT 9999 BKN006 OVC030 14/12 Q1028 NOSIG RMK A3037",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "NOSIG"
    assert trend.translation == "no significant changes"
    assert (
        str(trend)
        == "no significant changes from 2022-02-05 04:00:00 until 2022-02-05 06:00:00"
    )
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 5
    assert trend.period_from.hour == 4
    assert trend.period_from.minute == 0
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 5
    assert trend.period_until.hour == 6
    assert trend.period_until.minute == 0
    assert trend.period_at == None


def test_trend_code_tempo():
    metar = Metar(
        "SPECI MMMX 051347Z 07006KT 5SM SKC 05/02 A3044 TEMPO 3SM HZ RMK HZY ISOL SC LWR VSBY N",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "TEMPO"
    assert trend.translation == "temporary"
    assert str(trend) == "temporary from 2022-02-05 13:47:00 until 2022-02-05 15:47:00"
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 5
    assert trend.period_from.hour == 13
    assert trend.period_from.minute == 47
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 5
    assert trend.period_until.hour == 15
    assert trend.period_until.minute == 47
    assert trend.period_at == None


def test_trend_code_becmg():
    metar = Metar(
        "SPECI LYTV 040930Z VRB02KT CAVOK 12/M01 Q1023 BECMG 14005KT",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "BECMG"
    assert trend.translation == "becoming"
    assert str(trend) == "becoming from 2022-02-04 09:30:00 until 2022-02-04 11:30:00"
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 4
    assert trend.period_from.hour == 9
    assert trend.period_from.minute == 30
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 4
    assert trend.period_until.hour == 11
    assert trend.period_until.minute == 30
    assert trend.period_at == None


def test_trend_code_becmg_with_from_period():
    metar = Metar(
        "SPECI LTFG 061350Z 17004KT 120V240 9999 SCT030 16/09 Q1020 BECMG FM1410 22005KT",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "BECMG FM1410"
    assert trend.translation == "becoming"
    assert str(trend) == "becoming from 2022-02-06 14:10:00 until 2022-02-06 15:50:00"
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 6
    assert trend.period_from.hour == 14
    assert trend.period_from.minute == 10
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 6
    assert trend.period_until.hour == 15
    assert trend.period_until.minute == 50
    assert trend.period_at == None


def test_trend_code_tempo_with_from_and_until_periods():
    metar = Metar(
        "KRWV 062335Z 00000KT 10SM SCT015 14/02 A3018 TEMPO FM0000 TL0100 BKN015 TL0RMK AO2 T01380018",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "TEMPO FM0000 TL0100"
    assert trend.translation == "temporary"
    assert str(trend) == "temporary from 2022-02-07 00:00:00 until 2022-02-07 01:00:00"
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 7
    assert trend.period_from.hour == 0
    assert trend.period_from.minute == 0
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 7
    assert trend.period_until.hour == 1
    assert trend.period_until.minute == 0
    assert trend.period_at == None


def test_trend_code_becmg_with_at_period():
    metar = Metar(
        "LFPB 070000Z 28008KT 260V320 9999 SCT030 SCT039 BKN047 09/05 Q1017 BECMG AT0030 25020G30KT",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == "BECMG AT0030"
    assert trend.translation == "becoming"
    assert str(trend) == "becoming at 2022-02-07 00:30:00"
    assert trend.period_from.year == 2022
    assert trend.period_from.month == 2
    assert trend.period_from.day == 7
    assert trend.period_from.hour == 0
    assert trend.period_from.minute == 0
    assert trend.period_until.year == 2022
    assert trend.period_until.month == 2
    assert trend.period_until.day == 7
    assert trend.period_until.hour == 2
    assert trend.period_until.minute == 0
    assert trend.period_at.year == 2022
    assert trend.period_at.month == 2
    assert trend.period_at.day == 7
    assert trend.period_at.hour == 0
    assert trend.period_at.minute == 30


def test_no_trend():
    metar = Metar(
        "MRLM 072200Z 02006KT CAVOK 28/21 A2986",
        year=_year,
        month=_month,
    )
    trend = metar.trend

    assert trend.code == None
    assert trend.translation == None
    assert str(trend) == ""
