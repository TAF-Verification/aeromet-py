from aeromet_py import Metar


def test_trend_code_nosig():
    metar = Metar(
        "METAR SEQM 050400Z 04010KT 9999 BKN006 OVC030 14/12 Q1028 NOSIG RMK A3037"
    )
    trend = metar.trend

    assert trend.code == "NOSIG"
    assert trend.translation == "no significant changes"


def test_trend_code_tempo():
    metar = Metar(
        "SPECI MMMX 051347Z 07006KT 5SM SKC 05/02 A3044 TEMPO 3SM HZ RMK HZY ISOL SC LWR VSBY N"
    )
    trend = metar.trend

    assert trend.code == "TEMPO"
    assert trend.translation == "temporary"


def test_trend_code_becmg():
    metar = Metar("SPECI LYTV 040930Z VRB02KT CAVOK 12/M01 Q1023 BECMG 14005KT")
    trend = metar.trend

    assert trend.code == "BECMG"
    assert trend.translation == "becoming"
