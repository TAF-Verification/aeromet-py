from aeromet_py import Metar

metar = Metar("METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004 RMK TS TO S NOSIG")
sections = ["METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004",  "NOSIG", "RMK TS TO S"]

def test_sections():
    assert metar.sections == sections