import pytest

from aeromet_py import Metar
from aeromet_py.models import RangeError

_year: int = 2022
_month: int = 2


def test_weather_trend_code_nosig():
    metar = Metar(
        "METAR SEQM 050400Z 04010KT 9999 BKN006 OVC030 14/12 Q1028 NOSIG RMK A3037",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["NOSIG"]
    assert (
        str(trends)
        == "no significant changes from 2022-02-05 04:00:00 until 2022-02-05 06:00:00"
    )

    first = trends[0]
    assert first.code == "NOSIG"
    assert first.change_indicator.code == "NOSIG"
    assert first.change_indicator.translation == "no significant changes"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 5
    assert first.change_indicator.period_from.hour == 4
    assert first.change_indicator.period_from.minute == 0
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 5
    assert first.change_indicator.period_until.hour == 6
    assert first.change_indicator.period_until.minute == 0
    assert first.change_indicator.period_at == None

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_code_tempo():
    metar = Metar(
        "SPECI MMMX 051347Z 07006KT 5SM SKC 05/02 A3044 TEMPO 3SM HZ RMK HZY ISOL SC LWR VSBY N",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO 3SM HZ"]
    assert (
        str(trends) == "temporary from 2022-02-05 13:47:00 until 2022-02-05 15:47:00\n"
        "5.6 km\n"
        "haze"
    )

    first = trends[0]
    assert first.code == "TEMPO 3SM HZ"
    assert first.change_indicator.code == "TEMPO"
    assert first.change_indicator.translation == "temporary"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 5
    assert first.change_indicator.period_from.hour == 13
    assert first.change_indicator.period_from.minute == 47
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 5
    assert first.change_indicator.period_until.hour == 15
    assert first.change_indicator.period_until.minute == 47
    assert first.change_indicator.period_at == None

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_code_becmg():
    metar = Metar(
        "SPECI LYTV 040930Z VRB02KT CAVOK 12/M01 Q1023 BECMG 14005KT",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG 14005KT"]
    assert (
        str(trends) == "becoming from 2022-02-04 09:30:00 until 2022-02-04 11:30:00\n"
        "SE (140.0°) 5.0 kt"
    )

    first = trends[0]
    assert first.code == "BECMG 14005KT"
    assert first.change_indicator.code == "BECMG"
    assert first.change_indicator.translation == "becoming"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 4
    assert first.change_indicator.period_from.hour == 9
    assert first.change_indicator.period_from.minute == 30
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 4
    assert first.change_indicator.period_until.hour == 11
    assert first.change_indicator.period_until.minute == 30
    assert first.change_indicator.period_at == None

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_code_becmg_with_from_period():
    metar = Metar(
        "SPECI LTFG 061350Z 17004KT 120V240 9999 SCT030 16/09 Q1020 BECMG FM1410 22005KT",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG FM1410 22005KT"]
    assert (
        str(trends) == "becoming from 2022-02-06 14:10:00 until 2022-02-06 15:50:00\n"
        "SW (220.0°) 5.0 kt"
    )

    first = trends[0]
    assert first.code == "BECMG FM1410 22005KT"
    assert first.change_indicator.code == "BECMG FM1410"
    assert first.change_indicator.translation == "becoming"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 6
    assert first.change_indicator.period_from.hour == 14
    assert first.change_indicator.period_from.minute == 10
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 6
    assert first.change_indicator.period_until.hour == 15
    assert first.change_indicator.period_until.minute == 50
    assert first.change_indicator.period_at == None

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_code_tempo_with_from_and_until_periods():
    metar = Metar(
        "METAR KRWV 062335Z 00000KT 10SM SCT015 14/02 A3018 TEMPO FM0000 TL0100 BKN015 RMK AO2 T01380018",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["TEMPO FM0000 TL0100 BKN015"]
    assert (
        str(trends) == "temporary from 2022-02-07 00:00:00 until 2022-02-07 01:00:00\n"
        "broken at 1500.0 feet"
    )

    first = trends[0]
    assert first.code == "TEMPO FM0000 TL0100 BKN015"
    assert first.change_indicator.code == "TEMPO FM0000 TL0100"
    assert first.change_indicator.translation == "temporary"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 7
    assert first.change_indicator.period_from.hour == 0
    assert first.change_indicator.period_from.minute == 0
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 7
    assert first.change_indicator.period_until.hour == 1
    assert first.change_indicator.period_until.minute == 0
    assert first.change_indicator.period_at == None

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_code_becmg_with_at_period():
    metar = Metar(
        "METAR LFPB 070000Z 28008KT 260V320 9999 SCT030 SCT039 BKN047 09/05 Q1017 BECMG AT0030 25020G30KT",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG AT0030 25020G30KT"]
    assert (
        str(trends) == "becoming at 2022-02-07 00:30:00\n"
        "WSW (250.0°) 20.0 kt gust of 30.0 kt"
    )

    first = trends[0]
    assert first.code == "BECMG AT0030 25020G30KT"
    assert first.change_indicator.code == "BECMG AT0030"
    assert first.change_indicator.translation == "becoming"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 7
    assert first.change_indicator.period_from.hour == 0
    assert first.change_indicator.period_from.minute == 0
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 7
    assert first.change_indicator.period_until.hour == 2
    assert first.change_indicator.period_until.minute == 0
    assert first.change_indicator.period_at.year == 2022
    assert first.change_indicator.period_at.month == 2
    assert first.change_indicator.period_at.day == 7
    assert first.change_indicator.period_at.hour == 0
    assert first.change_indicator.period_at.minute == 30

    with pytest.raises(IndexError):
        assert trends[1].code == None


def test_weather_trend_with_two_changes():
    metar = Metar(
        "METAR UNOO 150100Z 36007MPS 2100 R07/2000N -SN BLSN BKN005 BKN020 M15/M18 Q1010 R07/492045 BECMG FM0130 5000 TEMPO FM0215 TL0245 BKN010 RMK OBST OBSC QFE749",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == ["BECMG FM0130 5000", "TEMPO FM0215 TL0245 BKN010"]
    assert str(trends) == (
        "becoming from 2022-02-15 01:30:00 until 2022-02-15 03:00:00\n"
        "5.0 km\n"
        "temporary from 2022-02-15 02:15:00 until 2022-02-15 02:45:00\n"
        "broken at 1000.0 feet"
    )

    first = trends[0]
    assert first.code == "BECMG FM0130 5000"
    assert first.change_indicator.code == "BECMG FM0130"
    assert first.change_indicator.translation == "becoming"
    assert first.change_indicator.period_from.year == 2022
    assert first.change_indicator.period_from.month == 2
    assert first.change_indicator.period_from.day == 15
    assert first.change_indicator.period_from.hour == 1
    assert first.change_indicator.period_from.minute == 30
    assert first.change_indicator.period_until.year == 2022
    assert first.change_indicator.period_until.month == 2
    assert first.change_indicator.period_until.day == 15
    assert first.change_indicator.period_until.hour == 3
    assert first.change_indicator.period_until.minute == 0
    assert first.change_indicator.period_at == None

    second = trends[1]
    assert second.code == "TEMPO FM0215 TL0245 BKN010"
    assert second.change_indicator.code == "TEMPO FM0215 TL0245"
    assert second.change_indicator.translation == "temporary"
    assert second.change_indicator.period_from.year == 2022
    assert second.change_indicator.period_from.month == 2
    assert second.change_indicator.period_from.day == 15
    assert second.change_indicator.period_from.hour == 2
    assert second.change_indicator.period_from.minute == 15
    assert second.change_indicator.period_until.year == 2022
    assert second.change_indicator.period_until.month == 2
    assert second.change_indicator.period_until.day == 15
    assert second.change_indicator.period_until.hour == 2
    assert second.change_indicator.period_until.minute == 45
    assert second.change_indicator.period_at == None

    with pytest.raises(RangeError):
        assert trends[2].code == None


def test_no_weather_trend():
    metar = Metar(
        "MRLM 072200Z 02006KT CAVOK 28/21 A2986",
        year=_year,
        month=_month,
    )
    trends = metar.weather_trends

    assert trends.codes == []
    assert str(trends) == ""

    with pytest.raises(IndexError):
        assert trends[0].code == None
