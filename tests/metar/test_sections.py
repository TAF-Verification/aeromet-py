from aeromet_py import Metar

metar = Metar(
    "\t\t\tMETAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004 RMK TS TO S NOSIG\n\n"
)
sections = [
    "METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004",
    "NOSIG",
    "RMK TS TO S",
]


def test_sections():
    assert metar.sections == sections
    assert metar.body == sections[0]
    assert metar.trend_forecast == sections[1]
    assert metar.remark == sections[2]
