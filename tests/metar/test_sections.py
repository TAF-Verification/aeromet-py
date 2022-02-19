from aeromet_py import Metar

TEXT: str = "\t\t\t{}\n\n"


def test_sections_weather_trend_nosig():
    code: str = "METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004 RMK TS TO S NOSIG"
    metar = Metar(TEXT.format(code))
    sections = [
        "METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004",
        "NOSIG",
        "RMK TS TO S",
    ]
    assert metar.sections == sections
    assert metar.body == sections[0]
    assert metar.trend == sections[1]
    assert metar.remark == sections[2]


def test_sections_weather_trend_tempo():
    code: str = "METAR MMTJ 180842Z 12006KT 7SM SKC 11/M04 A3027\tTEMPO 25005KT 5SM HZ\tRMK SLP258 54000 941"
    metar = Metar(TEXT.format(code))
    sections = [
        "METAR MMTJ 180842Z 12006KT 7SM SKC 11/M04 A3027",
        "TEMPO 25005KT 5SM HZ",
        "RMK SLP258 54000 941",
    ]
    assert metar.sections == sections
    assert metar.body == sections[0]
    assert metar.trend == sections[1]
    assert metar.remark == sections[2]


def test_sections_two_weather_trends():
    code: str = "SPECI LTBG 181003Z VRB02KT 9999 -SHRA BKN030 BKN100 09/09 Q1013 RESHRA\nBECMG TL1045 RA TEMPO FM1100 DZ RMK RWY18 04006KT 360V070"
    metar = Metar(TEXT.format(code))
    sections = [
        "SPECI LTBG 181003Z VRB02KT 9999 -SHRA BKN030 BKN100 09/09 Q1013 RESHRA",
        "BECMG TL1045 RA TEMPO FM1100 DZ",
        "RMK RWY18 04006KT 360V070",
    ]
    assert metar.sections == sections
    assert metar.body == sections[0]
    assert metar.trend == sections[1]
    assert metar.remark == sections[2]
